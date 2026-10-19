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
The background is transparent and the two ink colours are Iosevka's own, so
the specimen sits next to Iosevka's documentation without clashing.
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

# Code in the body colour, comment in the accent, as a syntax theme would.
CODE = "float Fox.quick(h);  "
COMMENT = "// 다람쥐 헌 쳇바퀴에 타고파"

# Iosevka's own specimen palette (images/ss-*.{light,dark}.svg).
PALETTES = {
    "light": {"ink": "#20242e", "accent": "#048fbf"},
    "dark": {"ink": "#dee4e3", "accent": "#03aee9"},
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--font-dir", type=Path, default=ROOT / "dist")
    p.add_argument("--output-dir", type=Path, default=ROOT / "assets")
    p.add_argument("--prefix", default="presevka-specimen")
    p.add_argument("--size", type=int, default=30, help="글자 크기(px)")
    p.add_argument("--line-height", type=float, default=1.62)
    p.add_argument("--label-size", type=int, default=13)
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

    label_font = fonts["Regular"]
    upem = label_font["head"].unitsPerEm
    scale = args.size / upem
    label_scale = args.label_size / upem

    # Measure once so every line shares the same left edge.
    _, text_end = run_path(label_font, CODE + COMMENT, 0)
    label_widths = [run_path(label_font, w, 0)[1] for w in PRESEVKA_WEIGHTS]
    gutter = max(label_widths) * label_scale + args.size * 0.9
    pad = args.size * 0.7
    width = gutter + text_end * scale + pad
    step = args.size * args.line_height
    height = pad + step * len(PRESEVKA_WEIGHTS)

    rows = []
    for index, weight in enumerate(PRESEVKA_WEIGHTS):
        font = fonts[weight]
        baseline = pad + step * index + args.size * 0.74
        code, end = run_path(font, CODE, 0)
        comment, _ = run_path(font, COMMENT, end)
        label, label_end = run_path(label_font, weight, 0)
        label_x = gutter - args.size * 0.9 - label_end * label_scale
        rows.append(
            f'  <g transform="translate({label_x:.1f} {baseline:.1f}) '
            f'scale({label_scale:.5f} -{label_scale:.5f})" '
            f'fill="{palette["ink"]}" fill-opacity=".45">'
            f'<path d="{label}"/></g>\n'
            f'  <g transform="translate({gutter:.1f} {baseline:.1f}) '
            f'scale({scale:.5f} -{scale:.5f})">'
            f'<path fill="{palette["ink"]}" d="{code}"/>'
            f'<path fill="{palette["accent"]}" d="{comment}"/></g>'
        )

    for font in fonts.values():
        font.close()

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" '
        f'aria-label="Presevka 굵기별 견본: {CODE.strip()} {COMMENT}">\n'
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
