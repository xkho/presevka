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

# Pinned to a commit rather than to a tag or to a branch. A tag would not do:
# the samples were added after v0.8.0 was cut, so they are in no earlier tag,
# and a branch would quietly restyle every past release the next time the
# artwork is redrawn. A commit cannot move.
IMAGE = """\
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{base}/presevka-code-v{version}-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="{base}/presevka-code-v{version}-light.svg">
    <img alt="Presevka v{version} 코드 견본 / code sample" src="{base}/presevka-code-v{version}-light.svg" width="100%">
  </picture>
</p>
"""

INTRO = """\
Iosevka의 라틴에 Pretendard의 한글을 얹은 고정폭 글꼴입니다. 한글 한 칸이
라틴 두 칸에 정확히 대응하고, 아홉 굵기 모두에서 한글과 라틴이 같은 굵기로
읽히도록 맞췄습니다.

A monospace font that sets Pretendard's Hangul against Iosevka's Latin. One
Hangul cell is exactly two Latin cells, and at every one of the nine weights
the two scripts are fitted to read as one weight.
"""

DOWNLOADS_HEAD = """\
## 다운로드 / Downloads

| 파일 / File | 용도 / Use |
| --- | --- |
"""

DOWNLOADS_TAIL = """\
개별 TTF 파일은 아래 assets 목록에서 따로 받을 수 있습니다.
Individual TTF faces are listed in the assets below.

라이선스 문서(`OFL.txt`, `THIRD_PARTY.md`, `FONTLOG.md`)는 각 아카이브에 함께 들어 있습니다.
Each archive ships with its licensing paperwork.
"""

NO_ARCHIVE = """\
## 다운로드 / Downloads

이 판본은 아카이브 없이 TTF 파일만 올라가 있습니다. 아래 assets 목록에서 받으세요.
This release predates the archives; the TTF faces are in the assets below.
"""

# The earliest releases shipped one zip, or none at all, under names that have
# since changed. The table is built from what a release actually carries rather
# than from the current naming, so an old page does not point at a file that
# was never there.
WEB = "웹폰트 / Web fonts"
DESKTOP = "데스크톱 설치용, 9 weight × Upright/Italic 18개 페이스 / Desktop install, 18 faces"
DESKTOP_EARLY = "설치용 폰트 묶음 / The fonts, zipped"


def downloads(version: str, archives: list[str]) -> str:
    if not archives:
        return NO_ARCHIVE
    rows = []
    for name in archives:
        if "woff2" in name:
            use = WEB
        elif len(archives) > 1:
            use = DESKTOP
        else:
            use = DESKTOP_EARLY
        rows.append(f"| `{name}` | {use} |")
    return DOWNLOADS_HEAD + "\n".join(rows) + "\n\n" + DOWNLOADS_TAIL


FOOTER = """\
변경 이력은 각 아카이브의 `FONTLOG.md`에 있습니다.
The record of what changed is in `FONTLOG.md` inside each archive.
"""

FOOTER_NO_ARCHIVE = """\
변경 이력은 저장소의 [`FONTLOG.md`](https://github.com/xkho/presevka/blob/main/FONTLOG.md)에 있습니다.
The record of what changed is in the repository's `FONTLOG.md`.
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
    p.add_argument(
        "--intro",
        help="맨 앞에 올 소개. 생략하면 현재 판본을 설명하는 기본 문구를 씁니다. "
        "옛 릴리스에는 그때 참이던 문장을 따로 넘겨야 합니다.",
    )
    p.add_argument(
        "--image-base",
        help="견본 SVG가 놓인 주소. 주면 소개 다음에 이미지가 들어갑니다.",
    )
    p.add_argument(
        "--archive",
        action="append",
        dest="archives",
        help="이 릴리스에 실제로 올라간 아카이브 이름. 여러 번 줄 수 있고, "
        "한 번도 주지 않으면 현재 이름 규칙을 씁니다.",
    )
    p.add_argument("--output", type=Path)
    return p.parse_args()


def compose(
    version: str,
    summary: str | None,
    summary_en: str | None,
    image_base: str | None = None,
    intro: str | None = None,
    archives: list[str] | None = None,
) -> str:
    parts = [(intro or INTRO).rstrip() + "\n"]
    if image_base:
        parts.append(IMAGE.format(base=image_base.rstrip("/"), version=version))
    if archives is not None:
        archives = [name for name in archives if name]
    parts.append(
        downloads(
            version,
            archives
            if archives is not None
            else [
                f"Presevka-{version}-ttf.zip",
                f"Presevka-{version}-woff2.zip",
            ],
        )
    )
    if summary:
        changes = ["## 이번 변경 / Changes", "", summary]
        if summary_en:
            changes += ["", summary_en]
        parts.insert(len(parts) - 1, "\n".join(changes) + "\n")
    parts.append(FOOTER if archives is None or archives else FOOTER_NO_ARCHIVE)
    return "\n".join(parts)


def main() -> None:
    args = parse_args()
    body = compose(
        args.version,
        args.summary,
        args.summary_en,
        args.image_base,
        args.intro,
        args.archives,
    )
    if args.output:
        args.output.write_text(body, encoding="utf-8")
        print(f"release notes: {args.output}")
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
