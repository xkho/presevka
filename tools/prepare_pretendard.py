from __future__ import annotations

import argparse
import json
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.scaleUpem import scale_upem
from fontTools.varLib import instancer

from font_utils import (
    ALL_HANGUL_RANGES,
    EXPECTED_MODERN_SYLLABLES,
    PRESEVKA_HANGUL_CELL,
    PRESEVKA_HANGUL_EXTRA_WIDTH,
    PRESEVKA_HANGUL_OUTLINE_SCALE,
    PRESEVKA_LATIN_CELL,
    PRESEVKA_STEM_PROBE_HANGUL,
    PRESEVKA_STEM_PROBE_LATIN,
    STRICT_HANGUL_RANGES,
    best_cmap,
    glyph_bounds,
    in_ranges,
    latin_cell,
    stem_slack,
    stroke_width,
    target_hangul_stem,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Instantiate Pretendard Variable at the weight whose stem matches the "
            "Iosevka base, normalize it to the Iosevka UPM, and fit Hangul to "
            "exactly two 500-unit Latin cells."
        )
    )
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--base-font", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--report", type=Path)
    return p.parse_args()


def weight_axis(font: TTFont) -> tuple[float, float]:
    """Return the wght axis range of the Pretendard source."""
    if "fvar" not in font:
        raise RuntimeError(
            "Pretendard source is static. Point --input at PretendardVariable.ttf "
            "so the Hangul stem can be matched to the Iosevka base."
        )
    for axis in font["fvar"].axes:
        if axis.axisTag == "wght":
            return float(axis.minValue), float(axis.maxValue)
    raise RuntimeError("Pretendard source has no wght axis to match the stem on")


def solve_wght(font: TTFont, low: float, high: float, target: float) -> float:
    """Return the wght whose Hangul stem is `target` units wide.

    The stem grows monotonically along the axis, so a bisection converges on it;
    a target outside the axis clamps to the nearest end, which is what happens
    at Thin, where Pretendard cannot be drawn as light as Iosevka.
    """

    def stem(value: float) -> float:
        return stroke_width(font, PRESEVKA_STEM_PROBE_HANGUL, location={"wght": value})

    if stem(low) >= target:
        return low
    if stem(high) <= target:
        return high
    while high - low > 0.05:
        mid = (low + high) / 2.0
        if stem(mid) < target:
            low = mid
        else:
            high = mid
    return round((low + high) / 2.0, 1)


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    base = TTFont(args.base_font)
    source = TTFont(args.input)
    try:
        if "OS/2" not in base or "OS/2" not in source:
            raise RuntimeError("both base and donor must contain an OS/2 table")
        base_weight = int(base["OS/2"].usWeightClass)
        axis_low, axis_high = weight_axis(source)

        # Match the stems before anything else. The target is a fraction of the
        # Latin stem rather than the whole of it, and the fit further down
        # enlarges every Hangul outline, taking its vertical stems with it,
        # so aim the axis lighter by however much the width grows.
        latin_stem = stroke_width(base, PRESEVKA_STEM_PROBE_LATIN)
        wanted_stem = target_hangul_stem(latin_stem)
        target_stem = wanted_stem / (
            PRESEVKA_HANGUL_OUTLINE_SCALE * PRESEVKA_HANGUL_EXTRA_WIDTH
        )
        matched_wght = solve_wght(source, axis_low, axis_high, target_stem)
        at_axis_floor = matched_wght <= axis_low

        instancer.instantiateVariableFont(
            source, {"wght": matched_wght}, inplace=True, updateFontNames=False
        )
        if "glyf" not in source:
            raise RuntimeError("instantiated Pretendard has no glyf outlines")
        # The instancer stamps round(matched_wght) into OS/2. This donor belongs
        # to the Iosevka weight it was fitted to, and merge_fonts.py requires the
        # two weight classes to agree.
        source["OS/2"].usWeightClass = base_weight

        target_upem = int(base["head"].unitsPerEm)
        cell = latin_cell(base)
        target_advance = cell * 2

        if cell != PRESEVKA_LATIN_CELL:
            raise RuntimeError(
                f"expected Iosevka Latin cell {PRESEVKA_LATIN_CELL}, got {cell}; "
                "refusing mismatched build"
            )
        if target_upem != 1000:
            raise RuntimeError(
                f"expected Iosevka UPM 1000, got {target_upem}; "
                "update math deliberately"
            )
        if target_advance != PRESEVKA_HANGUL_CELL:
            raise RuntimeError(
                f"expected target Hangul advance {PRESEVKA_HANGUL_CELL}, "
                f"got {target_advance}"
            )
        source_upem = int(source["head"].unitsPerEm)
        cmap = best_cmap(source)
        hmtx = source["hmtx"]

        modern_names = {
            name
            for cp, name in cmap.items()
            if 0xAC00 <= cp <= 0xD7A3 and name in hmtx.metrics
        }
        if len(modern_names) != EXPECTED_MODERN_SYLLABLES:
            raise RuntimeError(
                f"Pretendard source has {len(modern_names)} modern Hangul glyphs; "
                f"expected {EXPECTED_MODERN_SYLLABLES}"
            )

        modern_advances = {hmtx.metrics[name][0] for name in modern_names}
        if len(modern_advances) != 1:
            sample = sorted(modern_advances)[:20]
            raise RuntimeError(
                "Pretendard modern Hangul is not fixed-width; advances=" + repr(sample)
            )
        source_hangul_advance = modern_advances.pop()

        hangul_names = {
            name
            for cp, name in cmap.items()
            if in_ranges(cp, ALL_HANGUL_RANGES) and name in hmtx.metrics
        }

        # The source outlines changed, so source hints/signatures are no longer
        # valid, and STAT describes a variable family this donor is no longer in.
        for tag in ("fpgm", "prep", "cvt ", "DSIG", "STAT"):
            if tag in source:
                del source[tag]
        source["glyf"].removeHinting()

        if source_upem != target_upem:
            scale_upem(source, target_upem)

        # Modern syllables + compatibility jamo are strict 2-cell characters.
        cmap = best_cmap(source)
        hmtx = source["hmtx"]
        glyf = source["glyf"]
        strict_names = {
            name
            for cp, name in cmap.items()
            if in_ranges(cp, STRICT_HANGUL_RANGES) and name in hmtx.metrics
        }

        for name in strict_names:
            glyph = glyf[name]
            glyph.recalcBounds(glyf)
            old_advance, old_lsb = hmtx.metrics[name]
            dx = (target_advance - old_advance) / 2.0
            if dx:
                recording = DecomposingRecordingPen(source.getGlyphSet())
                source.getGlyphSet()[name].draw(recording)
                pen = TTGlyphPen(None)
                recording.replay(TransformPen(pen, Transform(1, 0, 0, 1, dx, 0)))
                glyph = pen.glyph()
                glyph.recalcBounds(glyf)
                glyf[name] = glyph
            hmtx.metrics[name] = (
                target_advance,
                int(getattr(glyph, "xMin", old_lsb + round(dx))),
            )

        # Enlarge every Hangul/Jamo outline, then widen it further, and centre
        # it in the 1000-unit advance; the remainder becomes side bearings.
        #
        # Vertically the block is placed rather than merely scaled. Hangul is
        # drawn centred in its own square, not sitting on the Latin baseline, so
        # what has to line up is the two inks' optical centres: the mean centre
        # of the Hangul against half the Latin's cap height. Deriving it here
        # keeps the two together when either the cap or the enlargement moves.
        fit_center = target_advance / 2.0
        strict_bounds = []
        ink_centers = []
        for name in strict_names:
            glyph = glyf[name]
            glyph.recalcBounds(glyf)
            if getattr(glyph, "numberOfContours", 0) != 0:
                strict_bounds.append((glyph.xMin, glyph.xMax))
                ink_centers.append((glyph.yMin + glyph.yMax) / 2.0)

        if not strict_bounds:
            raise RuntimeError("no strict Hangul outlines available for ink fitting")
        max_radius_before = max(
            fit_center - min(x_min for x_min, _ in strict_bounds),
            max(x_max for _, x_max in strict_bounds) - fit_center,
        )
        outline_scale = PRESEVKA_HANGUL_OUTLINE_SCALE
        width_scale = outline_scale * PRESEVKA_HANGUL_EXTRA_WIDTH
        ink_middle = sum(ink_centers) / len(ink_centers)
        base_cap = glyph_bounds(base, best_cmap(base)[ord("H")])[3]
        latin_middle = base_cap / 2.0
        y_shift = latin_middle - ink_middle * outline_scale
        expected_ink_radius = max_radius_before * width_scale
        fit_glyph_set = source.getGlyphSet()
        for name in hangul_names:
            advance, _ = hmtx.metrics[name]
            center = advance / 2.0
            x_shift = center * (1.0 - width_scale)
            recording = DecomposingRecordingPen(fit_glyph_set)
            fit_glyph_set[name].draw(recording)
            pen = TTGlyphPen(None)
            recording.replay(
                TransformPen(
                    pen,
                    Transform(width_scale, 0, 0, outline_scale, x_shift, y_shift),
                )
            )
            glyph = pen.glyph()
            glyph.recalcBounds(glyf)
            glyf[name] = glyph
            hmtx.metrics[name] = (advance, glyph.xMin)

        source.save(args.output)

        check = TTFont(args.output)
        try:
            if check["head"].unitsPerEm != target_upem:
                raise RuntimeError("prepared donor UPM verification failed")
            check_cmap = best_cmap(check)
            check_hmtx = check["hmtx"]
            check_glyf = check["glyf"]
            widths = {
                check_hmtx.metrics[name][0]
                for cp, name in check_cmap.items()
                if in_ranges(cp, STRICT_HANGUL_RANGES) and name in check_hmtx.metrics
            }
            if widths != {target_advance}:
                raise RuntimeError(
                    f"prepared donor width verification failed: {sorted(widths)}"
                )
            check_bounds = []
            for cp, name in check_cmap.items():
                if not in_ranges(cp, STRICT_HANGUL_RANGES):
                    continue
                glyph = check_glyf[name]
                glyph.recalcBounds(check_glyf)
                if getattr(glyph, "numberOfContours", 0) != 0:
                    check_bounds.append((glyph.xMin, glyph.xMax))
            actual_ink_radius = max(
                fit_center - min(x_min for x_min, _ in check_bounds),
                max(x_max for _, x_max in check_bounds) - fit_center,
            )
            if abs(actual_ink_radius - expected_ink_radius) > 1:
                raise RuntimeError(
                    "prepared donor ink envelope verification failed: "
                    f"expected radius {expected_ink_radius}, got {actual_ink_radius}"
                )
            hangul_stem = stroke_width(check, PRESEVKA_STEM_PROBE_HANGUL)
            slack = stem_slack(latin_stem, at_axis_floor=at_axis_floor)
            if abs(hangul_stem - wanted_stem) > slack:
                raise RuntimeError(
                    f"prepared donor stem {hangul_stem:.1f} misses its target "
                    f"{wanted_stem:.1f} by more than {slack:.1f} units "
                    f"(Latin {latin_stem:.1f}, wght {matched_wght})"
                )
        finally:
            check.close()

        report = {
            "weight_class": base_weight,
            "source_weight_axis": [axis_low, axis_high],
            "matched_wght": matched_wght,
            "matched_wght_at_axis_floor": at_axis_floor,
            "latin_stem": latin_stem,
            "target_hangul_stem": wanted_stem,
            "hangul_stem": hangul_stem,
            "hangul_stem_ratio": hangul_stem / latin_stem,
            "source_upem": source_upem,
            "source_modern_hangul_advance": source_hangul_advance,
            "source_modern_hangul_em": source_hangul_advance / source_upem,
            "target_upem": target_upem,
            "latin_cell": cell,
            "target_hangul_advance": target_advance,
            "target_hangul_em": target_advance / target_upem,
            "natural_max_ink_radius": max_radius_before,
            "outline_scale": outline_scale,
            "outline_width_scale": width_scale,
            "outline_change_percent": (outline_scale - 1.0) * 100.0,
            "latin_cap": base_cap,
            "hangul_ink_center": ink_middle * outline_scale + y_shift,
            "latin_ink_center": latin_middle,
            "actual_hangul_ink_width": actual_ink_radius * 2,
            "strict_hangul_glyphs": len(strict_names),
            "all_importable_hangul_glyphs": len(hangul_names),
        }
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        print(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"prepared: {args.output}")
    finally:
        base.close()
        source.close()


if __name__ == "__main__":
    main()
