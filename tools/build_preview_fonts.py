#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fonttools[woff]>=4.63.0",
#   "brotli>=1.1.0",
# ]
# ///

"""Cut the shipped faces down to what a preview page needs.

A released face carries every Hangul syllable and its hinting, which comes to
2.6 MB as woff2 and is far more than a page should pull before it can show
anything. Two things shrink it. Dropping the hinting, which a browser at
preview sizes does not use, takes a face to 1.3 MB. Splitting Latin from
Hangul takes the Latin alone to 160 KB.

The split is what makes the page quick rather than merely smaller. Each half
is declared with its own `unicode-range`, so a browser fetches the Hangul of a
weight only when it has Hangul of that weight to draw, and fetches nothing at
all for the eight weights nobody has asked to see. Declaring all nine costs
one request each for the Latin and nothing more until a reader moves the
slider.

Every OpenType feature is kept. The stylistic sets and character variants are
the thing this font has that the alternatives do not, so the page has to be
able to switch them on.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fontTools.subset import main as pyftsubset

from font_utils import PRESEVKA_WEIGHTS

ROOT = Path(__file__).resolve().parents[1]

# What a reader can type, minus Hangul: ASCII, Latin-1, the punctuation and
# arrows a specimen shows, and the maths a code sample runs into.
LATIN_RANGES = (
    "U+0020-007E,U+00A0-00FF,U+0100-017F,U+2000-206F,U+2070-209F,"
    "U+20A0-20BF,U+2100-214F,U+2190-21FF,U+2200-22FF,U+2300-23FF,"
    "U+25A0-25FF,U+2600-26FF,U+FB00-FB06"
)

# Hangul syllables, the compatibility jamo a keyboard produces on its own, and
# the fullwidth forms that turn up in Korean text.
HANGUL_RANGES = "U+1100-11FF,U+3000-303F,U+3130-318F,U+A960-A97F,U+AC00-D7A3,U+FF00-FFEF"

PARTS = {"latin": LATIN_RANGES, "hangul": HANGUL_RANGES}

# The nine-weight table shows every weight at once, which would otherwise pull
# every weight's Hangul before a reader has asked for any of it. It needs one
# line, so it gets a face cut to that line's characters and nothing else.
SPECIMEN = "float Fox.quick(h){ is_brown } // 다람쥐 헌 쳇바퀴에 타고파"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--font-dir", type=Path, default=ROOT / "dist")
    p.add_argument("--output-dir", type=Path, default=ROOT / "site" / "fonts")
    p.add_argument(
        "--slopes",
        default="Upright",
        help="쉼표로 구분. Upright,Italic 처럼 주면 이탤릭도 만듭니다.",
    )
    return p.parse_args()


def cut(source: Path, target: Path, unicodes: str | None, text: str = "") -> int:
    target.parent.mkdir(parents=True, exist_ok=True)
    argv = sys.argv
    sys.argv = [
        "pyftsubset",
        str(source),
        f"--text={text}" if text else f"--unicodes={unicodes}",
        # Keep every feature: the stylistic sets are the point.
        "--layout-features=*",
        "--flavor=woff2",
        "--desubroutinize",
        f"--output-file={target}",
    ]
    try:
        pyftsubset()
    finally:
        sys.argv = argv
    return target.stat().st_size


def main() -> None:
    args = parse_args()
    slopes = [s.strip() for s in args.slopes.split(",") if s.strip()]
    total = 0
    for weight in PRESEVKA_WEIGHTS:
        for slope in slopes:
            stem = weight if slope == "Upright" else f"{weight}Italic"
            stem = stem.replace("RegularItalic", "Italic")
            # A local build leaves TTFs behind; a release ships woff2, and
            # pyftsubset reads either.
            source = next(
                (
                    c
                    for c in (
                        args.font_dir / f"Presevka-{stem}.ttf",
                        args.font_dir / f"Presevka-{stem}.woff2",
                    )
                    if c.is_file()
                ),
                None,
            )
            if source is None:
                raise SystemExit(
                    f"no Presevka-{stem}.ttf or .woff2 in {args.font_dir}"
                )
            line = [f"{stem:18}"]
            for part, unicodes in PARTS.items():
                size = cut(
                    source, args.output_dir / f"Presevka-{stem}.{part}.woff2", unicodes
                )
                total += size
                line.append(f"{part} {size / 1024:7.1f} KB")
            size = cut(
                source,
                args.output_dir / f"Presevka-{stem}.spec.woff2",
                None,
                SPECIMEN,
            )
            total += size
            line.append(f"spec {size / 1024:5.1f} KB")
            print("  ".join(line))
    print(f"\n{args.output_dir}: {total / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
