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
PRESEVKA_VERSION = "0.8.1"
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
# Pretendard draws its Hangul for an advance of 864 of its em where the cell
# here is the full 1000, so 1000/864.26 = 1.1571 is the factor that would hand
# the donor over with every ratio it was drawn with intact: its proportion, and
# the 13.0% of the ink's width it leaves between one syllable and the next.
#
# That factor cannot be used, because Pretendard's own bold Hangul does not fit
# Pretendard's own cell. Its ink envelope runs to 104.1% of the advance at
# ExtraBold and 105.9% at Black, both on the same syllable, 뺐. A proportional
# font may let ink cross the advance and theirs does; a monospace cell cannot.
# Scaled proportionally, Black's ink would reach 6 units into the next cell and
# two syllables would overlap.
#
# So the fit has a ceiling, and the heaviest weight sets it: 1.1434 brings
# Black's widest syllable exactly to the cell wall. 0.8.0 took that ceiling, to
# within the 1.1297 that left Black 12 units of air on each side.
#
# It was still too much. Taking the ceiling is a decision about the Hangul
# alone, and the Hangul is not read alone: code is mostly lowercase Latin, and
# against lowercase the filled syllables read a size larger than the letters
# beside them. The comparison that shows it is how much of its own cell each
# script fills. At 1.1297 a mean syllable filled 85.8% of its 1000 while `o`
# filled 76.4% of its 500 -- 9.4 points apart, where 0.5.0 had them level.
#
# 1.11 closes about a sixth of that gap: 84.3% against the same 76.4%, 7.9
# points. It costs spacing, which goes from 16.6% of the ink to 18.6% against
# Pretendard's own 13.0%, and that is the trade this constant makes. Below
# about 1.09 the syllables of a word stop reading as one lump, which is the
# fault 0.7.0 was fixed to cure.
#
# Scaling both directions rather than only the width is what keeps the
# proportion at the donor's 0.890. Reaching the same spacing by widening alone
# took the syllables to 0.973, near enough square, and thickened the vertical
# stems while leaving the horizontals; scaling both asks the solver below for a
# lighter wght instead, which thins the two together.
#
# What it costs besides is height: 1.199 of the Latin cap, against the 1.216
# Pretendard keeps, 1.219 for Sarasa Gothic and 1.307 for D2Coding. The cause
# is not the Hangul but the Latin. Pretendard's cap is 0.818 of its Hangul
# advance where ours is 0.735, and matching that would need a cap of 818 units
# in a 500-unit cell. On this grid the two cannot both be had, so every Korean
# monospace picks a point on one line.
PRESEVKA_HANGUL_OUTLINE_SCALE = 1.11

# Then widen the Hangul alone, on top of that enlargement.
#
# 1.0, so nothing happens: the enlargement above already brings the spacing to
# what Pretendard drew, and anything further here only flattens the syllables.
# The factor is kept because the two scales are not interchangeable -- this one
# thickens the vertical stems without the horizontals -- and a build that wants
# to trade proportion for spacing has to say so separately from the fit.
PRESEVKA_HANGUL_EXTRA_WIDTH = 1.0

# Stroke matching. Pretendard's Hangul is instantiated from its variable font at
# the wght whose vertical stem hits PRESEVKA_HANGUL_STEM_RATIO of the Iosevka
# base's, measured on these two single-stroke probes: every other shared letter
# carries joins, curves or terminals that a bounding box cannot tell apart from
# the stem itself.
PRESEVKA_STEM_PROBE_LATIN = "|"
PRESEVKA_STEM_PROBE_HANGUL = "\u3163"  # HANGUL LETTER I, one bare vertical stroke

# Hangul is drawn slightly heavier than the Latin it sits beside.
#
# Total ink says the opposite — a syllable packs two or three jamo into one
# square — but the totals mislead, because the two scripts spread their ink
# over different bands. Latin lowercase, which is most of any code, sits
# between the baseline and the x-height; Hangul fills its square from the
# descender to above the cap. Measured by band, Latin lays 0.33 of its cell
# across 0 to 500 units where Hangul lays 0.21, so the Hangul reads pale
# exactly where the eye is.
#
# 1.10 overshot: it put the Hangul at 0.79 of the Latin over that band
# against D2Coding's 0.76, and widening the syllables added to it. 1.06
# lands on 0.76. Matching it outright would take 1.43, far enough up
# Pretendard's axis that Black's counters close; 1.10 leaves them at 0.64 of
# the glyph box. Pretendard draws its own Hangul at 0.92 and D2Coding at 1.18,
# so this sits between them. It also pulls Thin back towards the others:
# Pretendard's axis stops at 45 and cannot go thinner, and against the higher
# target that floor is 9% out rather than 36%.
PRESEVKA_HANGUL_STEM_RATIO = 0.96

# How far the two stems may end up apart: this fraction of the Latin stem, or
# PRESEVKA_STEM_SLACK units, whichever is larger. Coordinates are rounded on the
# way down from Pretendard's 2048-unit em, so the lightest weights need the
# absolute floor rather than a percentage.
PRESEVKA_STEM_TOLERANCE = 0.02
PRESEVKA_STEM_SLACK = 2.0

# Thin is the exception. Pretendard's wght axis stops at 45 and cannot be drawn
# as light as Iosevka Thin, so its Hangul stem overshoots: 27 units against the
# 19 the ratio asks for, a third heavier than the Latin it stands beside. The
# overshoot is the axis floor multiplied by the enlargement above, so it grows
# whenever the Hangul does, and this tolerance is only the accounting of a
# limit in the donor rather than a target of ours. Thinning Thin's outlines is
# the fix; until then the number here follows what the donor can actually do.
PRESEVKA_STEM_FLOOR_WEIGHTS = ("Thin",)
PRESEVKA_STEM_FLOOR_TOLERANCE = 0.40

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
