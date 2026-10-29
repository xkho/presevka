# FONTLOG for Presevka

This file records changes made in Presevka and acknowledges the upstream font
projects whose glyph designs it uses. Presevka is a Modified Version under the
SIL Open Font License, Version 1.1.

## Basic font information

Presevka combines an Iosevka programming-font base with Hangul glyphs prepared
from Pretendard. Its Latin advance width is 500 units and its strict Hangul
advance width is 1000 units in a 1000-unit em, so one Hangul cell occupies
exactly two Latin cells.

The public family name and all user-visible naming records use `Presevka`.
`Presevka` is a Reserved Font Name declared by Kwanho Lee (이관호).

## Upstream sources

- Iosevka v34.9.0, copyright Renzhi Li / The Iosevka Project Authors.
- Pretendard v1.3.9 variable font, copyright Kil Hyung-jin and the respective
  authors of its upstream glyph designs.

Exact notices and license terms are recorded in `OFL.txt` and
`THIRD_PARTY.md`.

## ChangeLog

### 29 October 2026 - Presevka 0.8.1 - Kwanho Lee (이관호)

- Drew the Hangul a little smaller: the enlargement over Pretendard's own
  drawing goes from 1.1297 to 1.11. 0.8.0 had taken as much of the proportional
  fit as the heaviest weight could hold, which is a decision about the Hangul
  on its own, and the Hangul is not read on its own. Code is mostly lowercase
  Latin, and against lowercase the filled syllables read a size larger than the
  letters beside them.
- What the eye was reporting is how much of its own cell each script fills. A
  mean syllable filled 85.8% of its 1000 units where `o` filled 76.4% of its
  500, 9.4 points apart; 0.5.0 had the two level. They now stand 7.9 points
  apart, at 84.3% against the same 76.4%.
- The cost is spacing, which goes from 16.6% of the ink's width to 18.6%
  against Pretendard's own 13.0%, and height, which comes to 1.199 of the cap
  where Pretendard keeps 1.216 and Sarasa Gothic 1.219.
- The Latin is untouched. The 792 cap, the 594 x-height and the side bearings
  at 1.05 of Iosevka's default all hold, as do advance widths, coverage and
  naming, so line and column counts hold.

### 27 October 2026 - Presevka 0.8.0 - Kwanho Lee (이관호)

- Hangul is now scaled by the factor that maps Pretendard's own 864-unit
  Hangul advance onto this font's 1000-unit cell, rather than by a figure
  chosen for how it looked. Pretendard's bold Hangul overruns even Pretendard's
  own advance, reaching 105.9% of it at Black, so the full factor cannot be
  used in a monospace cell; this takes as much of it as the heaviest weight
  holds. The syllables of a word now sit 16.6% of their ink apart, where 0.7.0
  left 23.0% and Pretendard itself leaves 13.0%.
- Dropped the separate horizontal widening. It had closed the same gap by
  flattening the syllables to 0.915 of their height; scaling both directions
  keeps Pretendard's own 0.888.
- Hangul is drawn at 0.96 of the Latin stem rather than 0.92.
- Raised the cap height from 735 to 792 and the x-height from 551 to 594, the
  same 0.75 proportion. The Hangul now stands at 1.220 of the cap, which is the
  1.211 Pretendard keeps and the 1.215 of Sarasa Gothic; against 0.7.0's cap it
  would have towered at 1.314.
- Widened the side bearings from 0.95 to 1.05 of Iosevka's default. The taller
  lowercase had eaten the air between letters: measured against the x-height,
  the gap had fallen to 0.178 where Iosevka keeps 0.215.
- Advance widths, coverage and naming are unchanged, so line and column counts
  hold.
- Known limitation: at Thin the Hangul stem lands a third heavier than the
  Latin. Pretendard's weight axis stops at 45 and cannot be drawn lighter, and
  the enlargement multiplies what the axis floor leaves over.

### 23 October 2026 - Presevka 0.7.0 - Kwanho Lee (이관호)

- Hangul is drawn at 0.92 of the Latin stem rather than matching it. A syllable
  packs two or three jamo into one square, so at an equal stroke it reads
  darker; Pretendard draws its own Hangul to the same ratio.
- Enlarged every Hangul outline by 7%, in both directions. Pretendard draws for
  an 864-unit advance and gets 1000 here, which had pushed the syllables of a
  word apart until it stopped reading as one lump.
- Restored Iosevka's 735 cap height, raising x-height to 551 for the 0.75 of
  Inter and Pretendard. 0.6.0's 707 left too little room to enlarge the Hangul.
- Advance widths, coverage and naming are unchanged, so line and column counts
  hold.

### 21 October 2026 - Presevka 0.6.0 - Kwanho Lee (이관호)

- Adopted Pretendard's Latin vertical metrics for the Iosevka base: cap height
  735 to 707, x-height 520 to 530. The two scripts now share an optical centre
  to within 1.5 units, where the Latin used to sit 15.5 units high.
- Lowercase therefore reaches 0.75 of the cap height, the proportion Inter and
  Pretendard both use, rather than Iosevka's 0.707. Most code is lowercase, so
  it reads a little larger despite the shorter capitals.
- The cap now stands at 0.81 of the Hangul's height, where Pretendard and
  Sarasa Gothic both place it.
- Advance widths, stroke weights, coverage and naming are unchanged, so line
  and column counts hold and only the Latin's height moved.

### 20 October 2026 - Presevka 0.5.0 - Kwanho Lee (이관호)

- Matched the Hangul stroke weight to the Latin one at every weight. Hangul now
  comes from Pretendard's variable font rather than its nine static weights: for
  each Iosevka weight the build measures the Latin stem (`|`), solves for the
  `wght` whose Hangul stem (`ㅣ`) equals it, and instantiates Pretendard there.
  Eight of the nine weights now land within one unit of their Latin stem, where
  before the Hangul ran 3% to 60% heavier. The solved axis positions are 149.3
  (ExtraLight), 278.9 (Light), 395.5 (Regular), 470.0 (Medium), 531.8
  (SemiBold), 606.1 (Bold), 680.3 (ExtraBold) and 754.6 (Black).
- Thin is the exception. Pretendard's `wght` axis stops at 45 and cannot be drawn
  as light as Iosevka Thin, so Thin clamps to the axis floor: a 23-unit Hangul
  stem against a 20-unit Latin one, down from 32.
- Horizontal strokes still differ, by design. Pretendard draws its horizontals
  lighter relative to its verticals than Iosevka does, so `ㅡ` measures 0.91 to
  1.00 of Iosevka's `-` depending on weight. Matching those as well would mean
  reshaping the Hangul outlines rather than choosing a point on an axis, so
  Pretendard's own stroke contrast is left intact.
- Hangul outlines no longer pass through a cubic-to-quadratic conversion. The
  static Pretendard releases are CFF and the previous build converted them with
  cu2qu; the variable font is already TrueType-flavoured, so its curves are used
  as drawn.
- Cell geometry, coverage and naming are unchanged: the 500/1000 advances, the
  2% horizontal optical correction, 11,172 modern syllables and 53 compatibility
  jamo all hold, and line and column counts in existing documents are unaffected.
  Only the Hangul weight moved, which narrows the ink envelopes to 858-908 units
  across the nine weights, where the heavier static weights reached 934.
- Added a stem check to the donor stage and to final-font QA. The prepared donor
  and every upright face must measure the same stem for `|` and `ㅣ`, within 2%
  or two units, whichever is larger; Thin is allowed its axis-floor difference.
  Italic faces are exempt because Iosevka slants `|` while the donated Hangul
  stays upright, so the probe cannot be compared there.

### 19 October 2026 - Presevka 0.4.1 - Kwanho Lee (이관호)

- Updated the Iosevka base from v34.8.0 to v34.9.0, which adds 176 characters
  and refines a few outlines. Of the glyphs both versions share, 35 changed:
  `!`, `?`, `D`, `G`, some accented Latin and five Greek letters. The changes
  are sub-unit — every advance is identical and no bounding box moves by more
  than one unit in a 1000-unit em — so the text colour and metrics hold.
  Presevka's own design, cell geometry and build are untouched, and no Hangul
  or jamo outline differs.

### 20 September 2026 - Presevka 0.4.0 - Kwanho Lee (이관호)

- Adopted Iosevka's stock character variants and its upstream-default 500-unit
  Latin cell for conventional half-em proportions. No stylistic set or
  character variant is overridden; custom builds may select their own.
- Set the strict Hangul advance to 1000 units, retaining the conventional
  relationship of one Hangul cell to two Latin cells.
- Preserved Pretendard's original weight-dependent horizontal proportions,
  applying the same minimal 2% enlargement to every Hangul and Jamo outline
  and centering it in the full-em cell. Resulting ink envelopes span 858–934
  units across the nine weights.
- Added TrueType hinting. By default ttfautohint runs over the merged font, so
  Latin and Hangul are both hinted; `PRESEVKA_HINT` selects `latin` (hint the
  Iosevka base only, leaving Pretendard outlines untouched), `gasp` (smoothing
  and dropout control only) or `none` (raw outlines).
- Corrected the imported Hangul range list. Hangul Jamo (U+1100-11FF) and Jamo
  Extended-A/B were listed but matched nothing, because the pinned Pretendard
  ships no conjoining jamo; the font covers 11,172 modern syllables and 53
  compatibility jamo. Text in NFD form therefore relies on the shaping engine
  to compose jamo back into precomposed syllables.
- Added build-time and final-font QA for the 500/1000 advances, the prepared
  Hangul geometry, upright Hangul outlines in Italic faces, Hangul coverage,
  and the hinting stage actually applied.
- Added WOFF2 output, release archives, and a tag-triggered release build.
- Documented how to select an Iosevka stylistic-set preset or override
  individual Latin glyph variants in custom builds.

### 14 September 2026 - Presevka 0.3.0 - Kwanho Lee (이관호)

- Added native Iosevka Italic faces for all nine weights, producing eighteen
  static Upright and Italic TTF files in total.
- Kept all imported Pretendard Hangul and Jamo outlines upright in Italic faces
  instead of applying synthetic slanting.
- Added slope-aware OpenType naming and metadata verification, including style
  linking, italic flags, and italic angle checks.
- Added QA comparison against the prepared upright Pretendard donor to prevent
  accidental Hangul slanting in future builds.

### 13 September 2026 - Presevka 0.2.0 - Kwanho Lee (이관호)

- Expanded the initial Regular-only build to nine static weights: Thin,
  ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold, and Black.
- Matched each Iosevka weight with the corresponding static Pretendard donor.
- Added weight-aware family naming and `OS/2` weight-class verification.
- Applied one uniform horizontal fit per heavy Hangul weight when necessary to
  keep every strict Hangul glyph inside its 864-unit cell.
- Updated installation and CI artifact packaging to include all nine weights.
- Limited the default Iosevka build concurrency to two jobs for predictable CI
  memory use, with `IOSEVKA_JOBS` available as an override.

### 13 September 2026 - Presevka 0.1.0 - Kwanho Lee (이관호)

- Built the Regular Upright Latin base from Iosevka with a custom 432/1000-em
  advance width, normal spacing, sans-serif construction, and upstream-default
  character variants.
- Used Iosevka's unhinted build because the outlines are subsequently modified
  and merged.
- Converted the static Pretendard Regular CFF outlines to TrueType `glyf`
  outlines when required.
- Normalized the Pretendard donor to a 1000-unit em.
- Horizontally scaled and centered imported Hangul outlines to fit an exact
  864-unit, two-Latin-cell advance.
- Imported modern Hangul syllables and supported Hangul/Jamo ranges from the
  prepared Pretendard donor into the Iosevka base.
- Removed invalidated source hinting and digital-signature data after outline
  modification.
- Recalculated Unicode/code-page coverage and expanded vertical metrics where
  required by imported Hangul outlines.
- Replaced source naming records with the public family name `Presevka` and
  recorded SIL OFL 1.1 licensing metadata.
- Added reproducible build, verification, QA, installation, and CI artifact
  packaging scripts.
