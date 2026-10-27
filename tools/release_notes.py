#!/usr/bin/env python3
"""Compose a release body.

The body is for whoever lands on the release page, which for this project is
often the first page they see: two thirds of the traffic arrives from a font
directory rather than from the README. So it opens by saying what the font is,
and leaves the downloads until after that.

What changed is deliberately thin here. GitHub appends its own "What's
Changed" from the merged pull requests and a link to the full diff, and
FONTLOG.md carries the measured record for anyone who wants it; repeating
either in between helps nobody. Pass --summary for a sentence or two in plain
words, or leave it out and the section does not appear.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from font_utils import PRESEVKA_VERSION

INTRO = """\
Iosevka의 라틴에 Pretendard의 한글을 얹은 고정폭 글꼴입니다. 한글 한 칸이
라틴 두 칸에 정확히 대응하고, 아홉 굵기 모두에서 한글과 라틴이 같은 굵기로
읽히도록 맞췄습니다.

A monospace font that sets Pretendard's Hangul against Iosevka's Latin. One
Hangul cell is exactly two Latin cells, and at every one of the nine weights
the two scripts are fitted to read as one weight.
"""

DOWNLOADS = """\
## 다운로드 / Downloads

| 파일 / File | 용도 / Use |
| --- | --- |
| `Presevka-{version}-ttf.zip` | 데스크톱 설치용, 9 weight × Upright/Italic 18개 페이스 / Desktop install, 18 faces |
| `Presevka-{version}-woff2.zip` | 웹폰트 / Web fonts |

개별 TTF 파일은 아래 assets 목록에서 따로 받을 수 있습니다.
Individual TTF faces are listed in the assets below.

라이선스 문서(`OFL.txt`, `THIRD_PARTY.md`, `FONTLOG.md`)는 각 아카이브에 함께 들어 있습니다.
Each archive ships with its licensing paperwork.
"""

FOOTER = """\
변경 이력은 각 아카이브의 `FONTLOG.md`에 있습니다.
The record of what changed is in `FONTLOG.md` inside each archive.
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--version", default=PRESEVKA_VERSION)
    p.add_argument(
        "--summary",
        help="이번에 무엇을 했는지 한두 문장. 수치는 FONTLOG에 두고 여기엔 쓰지 않습니다.",
    )
    p.add_argument(
        "--summary-en", help="같은 내용의 영문. --summary 없이는 쓰이지 않습니다."
    )
    p.add_argument("--output", type=Path)
    return p.parse_args()


def compose(version: str, summary: str | None, summary_en: str | None) -> str:
    parts = [INTRO, DOWNLOADS.format(version=version)]
    if summary:
        changes = ["## 이번 변경 / Changes", "", summary]
        if summary_en:
            changes += ["", summary_en]
        parts.insert(1, "\n".join(changes) + "\n")
    parts.append(FOOTER)
    return "\n".join(parts)


def main() -> None:
    args = parse_args()
    body = compose(args.version, args.summary, args.summary_en)
    if args.output:
        args.output.write_text(body, encoding="utf-8")
        print(f"release notes: {args.output}")
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
