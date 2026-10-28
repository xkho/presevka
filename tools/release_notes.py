#!/usr/bin/env python3
"""Compose a release body.

The body is for whoever lands on the release page, which for this project is
often the first page they see: two thirds of the traffic arrives from a font
directory rather than from the README. So it opens by saying what the font is,
and leaves the downloads until after that.

The two languages are kept apart rather than interleaved. A reader of either
one had been stepping over the other every few lines; now the page is Korean,
with a link at the top down to an English half that says the same things in
the same order.

Headings start at `###`. GitHub rules a line under `#` and `##`, and a short
release body with three of those reads as a stack of rules with text between
them. Nothing here is a document title, so nothing needs that weight.

What changed is deliberately thin. GitHub appends its own "What's Changed"
from the merged pull requests and a link to the full diff, and FONTLOG.md
carries the measured record for anyone who wants it; repeating either in
between helps nobody. Pass --summary for a sentence or two in plain words, or
leave it out and the section does not appear.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from font_utils import PRESEVKA_VERSION

# No width is set on the image: the sample is drawn at the size it should be
# read at, and stretching it to the column would undo that.
#
# Pinned to a commit rather than to a tag or to a branch. A tag would not do:
# a sample added after a release was cut is in no earlier tag, and a branch
# would quietly restyle every past release the next time the artwork is
# redrawn. A commit cannot move.
IMAGE = """\
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{base}/presevka-code-v{version}-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="{base}/presevka-code-v{version}-light.svg">
    <img alt="Presevka v{version} 코드 견본 / code sample" src="{base}/presevka-code-v{version}-light.svg">
  </picture>
</p>
"""

INTRO_EN = (
    "A monospace font that sets Pretendard's Hangul against Iosevka's Latin. "
    "One Hangul cell is exactly two Latin cells, and at every one of the nine "
    "weights the two scripts are fitted to read as one weight."
)

TAIL_KO = """\
개별 TTF 파일은 아래 assets 목록에서 따로 받을 수 있습니다.
라이선스 문서(`OFL.txt`, `THIRD_PARTY.md`, `FONTLOG.md`)는 각 아카이브에 함께 들어 있습니다.
변경 이력은 각 아카이브의 `FONTLOG.md`에 있습니다.
"""

TAIL_EN = """\
Individual TTF faces are listed in the assets below.
Each archive ships with its licensing paperwork.
The record of what changed is in `FONTLOG.md` inside each archive.
"""

TAIL_KO_NO_ARCHIVE = """\
변경 이력은 저장소의 [`FONTLOG.md`](https://github.com/xkho/presevka/blob/main/FONTLOG.md)에 있습니다.
"""

TAIL_EN_NO_ARCHIVE = """\
The record of what changed is in the repository's `FONTLOG.md`.
"""

NO_ARCHIVE_KO = "이 판본은 아카이브 없이 TTF 파일만 올라가 있습니다. 아래 assets 목록에서 받으세요."
NO_ARCHIVE_EN = "This release predates the archives; the TTF faces are in the assets below."

# The earliest releases shipped one zip, or none at all, under names that have
# since changed. The table is built from what a release actually carries rather
# than from the current naming, so an old page does not point at a file that
# was never there.
USES = {
    "web": ("웹폰트", "Web fonts"),
    "desktop": (
        "데스크톱 설치용, 9 weight × Upright/Italic 18개 페이스",
        "Desktop install, 18 faces",
    ),
    "early": ("설치용 폰트 묶음", "The fonts, zipped"),
}


# Where a release's own assets are served from. The name in the table is the
# link, so the table is the download rather than a label for one further down.
DOWNLOAD_URL = "https://github.com/xkho/presevka/releases/download/v{version}/{name}"


def downloads(version: str, archives: list[str], english: bool) -> str:
    """Return the downloads table in one language."""
    if not archives:
        return NO_ARCHIVE_EN if english else NO_ARCHIVE_KO
    header = (
        "| File | Use |\n| --- | --- |"
        if english
        else "| 파일 | 용도 |\n| --- | --- |"
    )
    rows = []
    for name in archives:
        if "woff2" in name:
            kind = "web"
        elif len(archives) > 1:
            kind = "desktop"
        else:
            kind = "early"
        url = DOWNLOAD_URL.format(version=version, name=name)
        rows.append(f"| [`{name}`]({url}) | {USES[kind][1 if english else 0]} |")
    return header + "\n" + "\n".join(rows)


def half(
    *,
    version: str,
    english: bool,
    summary: str | None,
    archives: list[str],
    image: str | None = None,
) -> list[str]:
    """Return one language's blocks, in the order they are read."""
    parts = []
    if image:
        parts.append(image.rstrip())
    if summary:
        parts.append(
            ("### What changed" if english else "### 이번 변경")
            + "\n\n"
            + summary.strip()
        )
    parts.append(
        ("### Downloads" if english else "### 다운로드")
        + "\n\n"
        + downloads(version, archives, english)
    )
    if archives:
        parts.append((TAIL_EN if english else TAIL_KO).strip())
    else:
        parts.append((TAIL_EN_NO_ARCHIVE if english else TAIL_KO_NO_ARCHIVE).strip())
    return parts


def compose(
    version: str,
    summary: str | None = None,
    summary_en: str | None = None,
    image_base: str | None = None,
    archives: list[str] | None = None,
) -> str:
    """Korean, a rule, the same again in English.

    No heading introduces either half and no sentence explains the font: the
    page is titled with the version and the reader came here from somewhere
    that already said what this is. A rule is enough to say the language has
    changed, and it costs no line of type.
    """
    if archives is None:
        archives = [f"Presevka-{version}-ttf.zip", f"Presevka-{version}-woff2.zip"]
    archives = [name for name in archives if name]
    image = (
        IMAGE.format(base=image_base.rstrip("/"), version=version)
        if image_base
        else None
    )

    parts = half(
        version=version,
        english=False,
        summary=summary,
        archives=archives,
        image=image,
    )
    parts.append("---")
    parts += half(
        version=version, english=True, summary=summary_en, archives=archives
    )
    return "\n\n".join(p for p in parts if p) + "\n"


def trailing(text: str) -> str:
    """Return the compare link out of GitHub's generated notes, and nothing else.

    What GitHub generates is a heading, a line per merged pull request, and a
    link to the diff. The heading is a second title for something this body
    already has a section for, and each pull request line says in English what
    the summary above said in both languages, with the author's name attached
    to a release only they publish. The diff link is the one part that is not
    said anywhere else.
    """
    for line in text.splitlines():
        if line.strip().startswith("**Full Changelog**"):
            return line.strip()
    return ""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--version", default=PRESEVKA_VERSION)
    p.add_argument(
        "--summary",
        help="이번에 무엇을 했는지 한두 문장. 수치는 FONTLOG에 두고 여기엔 쓰지 않습니다.",
    )
    p.add_argument("--summary-en", help="같은 내용의 영문.")
    p.add_argument(
        "--archive",
        action="append",
        dest="archives",
        help="이 릴리스에 실제로 올라간 아카이브 이름. 여러 번 줄 수 있고, "
        "한 번도 주지 않으면 현재 이름 규칙을 씁니다.",
    )
    p.add_argument(
        "--image-base",
        help="견본 SVG가 놓인 주소. 주면 소개 다음에 이미지가 들어갑니다.",
    )
    p.add_argument(
        "--append",
        type=Path,
        help="뒤에 붙일 파일. GitHub이 만든 What's Changed를 살릴 때 씁니다.",
    )
    p.add_argument("--output", type=Path)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    body = compose(
        args.version,
        args.summary,
        args.summary_en,
        args.image_base,
        args.archives,
    )
    if args.append and args.append.is_file():
        extra = trailing(args.append.read_text(encoding="utf-8"))
        if extra:
            body = body.rstrip() + "\n\n---\n\n" + extra + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
        print(f"release notes: {args.output}")
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
