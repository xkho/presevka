from __future__ import annotations

from collections.abc import Iterable

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


def _font_revision(version: str) -> float:
    """Derive head.fontRevision from the public version string.

    head.fontRevision is 16.16 fixed point, so 0.4.0 becomes 0.4 and 0.4.1
    becomes 0.401. Deriving it keeps the two from drifting apart.
    """
    major, minor, patch = (int(part) for part in version.split("."))
    return round(major + minor / 10 + patch / 1000, 3)


# Single source of truth. merge_fonts.py stamps these into every face and
# qa_font.py verifies them, so a release bump only happens here and in
# pyproject.toml.
PRESEVKA_VERSION = "0.7.0"
PRESEVKA_FONT_REVISION = _font_revision(PRESEVKA_VERSION)

PRESEVKA_WEIGHTS = (
    "Thin",
    "ExtraLight",
    "Light",
    "Regular",
    "Medium",
    "SemiBold",
    "Bold",
    "ExtraBold",
    "Black",
)
PRESEVKA_SLOPES = ("Upright", "Italic")
PRESEVKA_ITALIC_ANGLE = 9.4
PRESEVKA_POST_ITALIC_ANGLE = -float(round(PRESEVKA_ITALIC_ANGLE))
PRESEVKA_LATIN_CELL = 500
PRESEVKA_HANGUL_CELL = 1000

# Enlarge every Hangul and Jamo outline by this much, in both directions, and
# centre it in the full-em cell; the remainder becomes side bearings.
#
# The cell is 1000 units where Pretendard draws its Hangul for 864, so a
# syllable that filled its square now floats in a wider one. That pushes the
# syllables of a word apart until the word stops reading as one lump: against a
# 500-unit space, the gap between words comes to 3.28 times the gap between
# syllables, where Pretendard manages 3.66 and Sarasa Gothic 3.44. A 2%
# enlargement brings it to 3.46 and the ink to 797 units, which is where Sarasa
# sits, for 2% more height against the Latin.
#
# Scaling both directions rather than only the width is what keeps Pretendard's
# proportions: widening alone thickened the vertical stems while leaving the
# horizontals, which skewed the stroke contrast the donor was drawn with.
PRESEVKA_HANGUL_OUTLINE_SCALE = 1.07

# Stroke matching. Pretendard's Hangul is instantiated from its variable font at
# the wght whose vertical stem hits PRESEVKA_HANGUL_STEM_RATIO of the Iosevka
# base's, measured on these two single-stroke probes: every other shared letter
# carries joins, curves or terminals that a bounding box cannot tell apart from
# the stem itself.
PRESEVKA_STEM_PROBE_LATIN = "|"
PRESEVKA_STEM_PROBE_HANGUL = "\u3163"  # HANGUL LETTER I, one bare vertical stroke

# Hangul is drawn lighter than the Latin it sits beside, not equal to it. A
# syllable packs two or three jamo into one square, so at an equal stroke it
# lays down more ink per area and reads darker. Pretendard answers this by
# drawing its own Hangul at 0.92 of its Latin stem, and since 0.6.0 gave the
# Latin Pretendard's cap height the same figure carries over directly.
PRESEVKA_HANGUL_STEM_RATIO = 0.92

# How far the two stems may end up apart: this fraction of the Latin stem, or
# PRESEVKA_STEM_SLACK units, whichever is larger. Coordinates are rounded on the
# way down from Pretendard's 2048-unit em, so the lightest weights need the
# absolute floor rather than a percentage.
PRESEVKA_STEM_TOLERANCE = 0.02
PRESEVKA_STEM_SLACK = 2.0

# Thin is the exception. Pretendard's wght axis stops at 45 and cannot be drawn
# as light as Iosevka Thin, so its Hangul stem overshoots the target by about a
# quarter: 23.9 units against the 18.4 the ratio asks for.
PRESEVKA_STEM_FLOOR_WEIGHTS = ("Thin",)
PRESEVKA_STEM_FLOOR_TOLERANCE = 0.30

# Hinting stages, selected by the PRESEVKA_HINT environment variable.
#   full  - ttfautohint over the merged font, so Hangul is hinted too
#   latin - ttfautohint over the Iosevka base only, leaving Hangul unhinted
#   gasp  - no ttfautohint; only the gasp smoothing table
#   none  - ship raw outlines
# Every mode except "none" writes a gasp table.
PRESEVKA_HINT_MODES = ("full", "latin", "gasp", "none")
PRESEVKA_DEFAULT_HINT_MODE = "full"

# Strict 2-cell characters in the resulting monospace font.
STRICT_HANGUL_RANGES = (
    (0x3130, 0x318F),  # Hangul Compatibility Jamo
    (0xAC00, 0xD7A3),  # Modern precomposed Hangul syllables
)

# Every Hangul codepoint imported from the donor.
#
# Identical to the strict set: the pinned Pretendard provides only full-width
# standalone characters. Hangul Jamo (U+1100-11FF), Jamo Extended-A
# (U+A960-A97F) and Extended-B (U+D7B0-D7FF) used to be listed here but matched
# nothing, because Pretendard v1.3.9 ships no conjoining jamo at all. A donor
# that did provide them would extend this tuple but not STRICT_HANGUL_RANGES,
# since conjoining jamo must keep their own composing advances rather than be
# forced to two Latin cells. qa_font.py pins the expected coverage so such a
# donor fails the build instead of changing the font silently.
ALL_HANGUL_RANGES = STRICT_HANGUL_RANGES

# Blocks the pinned donor deliberately does not provide. qa_font.py fails the
# build if a future donor starts supplying them, because conjoining jamo need
# composing advances and jamo-composition GSUB rules rather than the two-cell
# treatment every imported glyph gets today.
DONOR_ABSENT_HANGUL_RANGES = (
    (0x1100, 0x11FF),  # Hangul Jamo (conjoining)
    (0xA960, 0xA97F),  # Hangul Jamo Extended-A
    (0xD7B0, 0xD7FF),  # Hangul Jamo Extended-B
)

# Coverage the pinned donor is expected to deliver, asserted after every merge.
EXPECTED_MODERN_SYLLABLES = 11172
EXPECTED_COMPAT_JAMO = 53


def in_ranges(cp: int, ranges: Iterable[tuple[int, int]]) -> bool:
    return any(start <= cp <= end for start, end in ranges)


def best_cmap(font: TTFont) -> dict[int, str]:
    cmap = font.getBestCmap()
    if cmap is None:
        raise RuntimeError("font has no usable Unicode cmap")
    return cmap


def glyph_bounds(font: TTFont, glyph_name: str):
    glyph_set = font.getGlyphSet()
    pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return pen.bounds


def stroke_width(font: TTFont, ch: str, *, location=None) -> float:
    """Return a single-stroke glyph's ink width, in 1000-unit em terms.

    Normalizing by UPM lets stems be compared across Iosevka's 1000-unit em and
    Pretendard's 2048-unit one. `location` reads the width at one point on a
    variable font's axes without instantiating the whole font.
    """
    name = best_cmap(font).get(ord(ch))
    if name is None:
        raise RuntimeError(f"font has no glyph for U+{ord(ch):04X}")
    glyph_set = font.getGlyphSet(location=location) if location else font.getGlyphSet()
    pen = BoundsPen(glyph_set)
    glyph_set[name].draw(pen)
    if pen.bounds is None:
        raise RuntimeError(f"U+{ord(ch):04X} has no outline to measure")
    x_min, _, x_max, _ = pen.bounds
    return (x_max - x_min) / font["head"].unitsPerEm * 1000.0


def target_hangul_stem(latin_stem: float) -> float:
    """Return the Hangul stem that balances a given Latin stem."""
    return latin_stem * PRESEVKA_HANGUL_STEM_RATIO


def stem_slack(latin_stem: float, *, at_axis_floor: bool) -> float:
    """Return how far a Hangul stem may sit from its target, in font units."""
    fraction = (
        PRESEVKA_STEM_FLOOR_TOLERANCE if at_axis_floor else PRESEVKA_STEM_TOLERANCE
    )
    return max(latin_stem * fraction, PRESEVKA_STEM_SLACK)


def latin_cell(font: TTFont) -> int:
    cmap = best_cmap(font)
    widths: list[int] = []
    for ch in "Mi0 ":
        name = cmap.get(ord(ch))
        if name is None:
            continue
        widths.append(font["hmtx"].metrics[name][0])
    if not widths or len(set(widths)) != 1:
        raise RuntimeError(f"base font is not monospaced for probe glyphs: {widths}")
    return widths[0]


def presevka_style_name(weight: str, slope: str) -> str:
    if slope == "Upright":
        return weight
    if weight == "Regular":
        return slope
    return f"{weight} {slope}"


def presevka_legacy_names(family: str, weight: str, slope: str) -> tuple[str, str]:
    if weight in {"Regular", "Bold"}:
        legacy_family = family
        legacy_weight = weight
    else:
        legacy_family = f"{family} {weight}"
        legacy_weight = "Regular"

    if slope == "Italic":
        legacy_subfamily = (
            "Italic" if legacy_weight == "Regular" else f"{legacy_weight} Italic"
        )
    else:
        legacy_subfamily = legacy_weight
    return legacy_family, legacy_subfamily
