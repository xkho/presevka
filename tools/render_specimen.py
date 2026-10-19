#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fonttools>=4.63.0",
# ]
# ///

"""Render the weight-axis specimen used in the README.

One line per weight, thin at the top and black at the bottom, drawn as SVG
outlines so the image stays sharp at any size and needs no font installed.
The background is transparent and the colours are Iosevka's own, so the
specimen sits next to Iosevka's documentation without clashing.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from font_utils import PRESEVKA_WEIGHTS

ROOT = Path(__file__).resolve().parents[1]

# Coloured the way an editor would: keyword, then the rest of the statement,
# then the comment.
KEYWORD = "float"
CODE = " Fox.quick(h);  "
COMMENT = "// 다람쥐 헌 쳇바퀴에 타고파"

# Iosevka's own colours. Ink and keyword come from images/weights.*.svg, the
# weight sample under Features in its README, which this specimen mirrors.
# The comment grey is from its website.
PALETTES = {
    "light": {"ink": "#20242e", "keyword": "#8757ad", "muted": "#6e7372"},
    "dark": {"ink": "#dee4e3", "keyword": "#b77fdb", "muted": "#acb0b0"},
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--font-dir", type=Path, default=ROOT / "dist")
    p.add_argument("--output-dir", type=Path, default=ROOT / "assets")
    p.add_argument("--prefix", default="presevka-specimen")
    p.add_argument("--size", type=int, default=30, help="글자 크기(px)")
    p.add_argument("--line-height", type=float, default=1.62)
    return p.parse_args()


def run_path(font: TTFont, text: str, start: float) -> tuple[str, float]:
    """Draw one run of text as a single SVG path, returning it and the pen x."""
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    metrics = font["hmtx"].metrics
    pen = SVGPathPen(glyphs)
    x = start
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            raise SystemExit(f"{font.reader.file.name} has no glyph for {ch!r}")
        glyphs[name].draw(TransformPen(pen, Transform(1, 0, 0, 1, x, 0)))
        x += metrics[name][0]
    return pen.getCommands(), x


def render(font_dir: Path, palette: dict[str, str], args: argparse.Namespace) -> str:
    fonts = {}
    for weight in PRESEVKA_WEIGHTS:
        path = font_dir / f"Presevka-{weight}.ttf"
        if not path.is_file():
            raise SystemExit(f"font not found: {path}\nBuild Presevka first.")
        fonts[weight] = TTFont(path)

    upem = fonts["Regular"]["head"].unitsPerEm
    scale = args.size / upem
    pad = args.size * 0.7
    _, text_end = run_path(fonts["Regular"], KEYWORD + CODE + COMMENT, 0)
    width = pad * 2 + text_end * scale
    step = args.size * args.line_height
    height = pad + step * len(PRESEVKA_WEIGHTS)

    rows = []
    for index, weight in enumerate(PRESEVKA_WEIGHTS):
        font = fonts[weight]
        baseline = pad + step * index + args.size * 0.74
        keyword, after_keyword = run_path(font, KEYWORD, 0)
        code, after_code = run_path(font, CODE, after_keyword)
        comment, _ = run_path(font, COMMENT, after_code)
        rows.append(
            f'  <g transform="translate({pad:.1f} {baseline:.1f}) '
            f'scale({scale:.5f} -{scale:.5f})">'
            f'<path fill="{palette["keyword"]}" d="{keyword}"/>'
            f'<path fill="{palette["ink"]}" d="{code}"/>'
            f'<path fill="{palette["muted"]}" d="{comment}"/></g>'
        )

    for font in fonts.values():
        font.close()

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" '
        f'aria-label="Presevka 굵기별 견본: {KEYWORD}{CODE.rstrip()} {COMMENT}">\n'
        + "\n".join(rows)
        + "\n</svg>\n"
    )


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for mode, palette in PALETTES.items():
        out = args.output_dir / f"{args.prefix}-{mode}.svg"
        out.write_text(render(args.font_dir, palette, args), encoding="utf-8")
        print(f"Wrote: {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
