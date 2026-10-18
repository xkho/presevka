from __future__ import annotations

import argparse
import re
from pathlib import Path

from font_utils import PRESEVKA_VERSION

# 영문: "### 20 September 2026 - Presevka 0.4.0 - Kwanho Lee (이관호)"
# 한국어: "### 2026년 9월 20일 - Presevka 0.4.0 - 이관호"
ENTRY = re.compile(
    r"^###\s+.*?\bPresevka\s+(?P<version>\d+\.\d+\.\d+)\b.*$", re.MULTILINE
)

BODY = """\
## 다운로드 / Downloads

| 파일 / File | 용도 / Use |
| --- | --- |
| `Presevka-{version}-ttf.zip` | 데스크톱 설치용, 9 weight × Upright/Italic 18개 페이스 / Desktop install, 18 faces |
| `Presevka-{version}-woff2.zip` | 웹폰트 / Web fonts |

개별 TTF 파일은 아래 assets 목록에서 따로 받을 수 있습니다.
Individual TTF faces are listed in the assets below.

라이선스 문서(`OFL.txt`, `THIRD_PARTY.md`, `FONTLOG.md`)는 각 아카이브에 함께 들어 있습니다.
Each archive ships with its licensing paperwork.

## 주요 변경 사항

{korean}

## Highlights

{english}

전체 변경 이력은 각 아카이브의 `FONTLOG.md`에 있습니다.
The complete history is in `FONTLOG.md` inside each archive.
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Compose the release body from this version's FONTLOG entries."
    )
    p.add_argument("--version", default=PRESEVKA_VERSION)
    p.add_argument("--fontlog", type=Path, default=Path("FONTLOG.md"))
    p.add_argument("--fontlog-ko", type=Path, default=Path("FONTLOG.ko.md"))
    p.add_argument(
        "--max-items",
        type=int,
        default=3,
        help="본문에 실을 항목 수. FONTLOG는 중요한 것부터 적습니다. 0이면 전부.",
    )
    p.add_argument("--output", type=Path)
    return p.parse_args()


def top_items(entry: str, limit: int) -> str:
    """Keep the first `limit` bullets, each of which may wrap over several lines."""
    if limit <= 0:
        return entry
    bullets: list[list[str]] = []
    for line in entry.splitlines():
        if line.startswith("- "):
            bullets.append([line])
        elif bullets:
            bullets[-1].append(line)
    if not bullets:
        return entry
    return "\n".join("\n".join(b).rstrip() for b in bullets[:limit])


def fontlog_entry(path: Path, version: str) -> str:
    """Return the bullet list one FONTLOG records for a version."""
    text = path.read_text(encoding="utf-8")
    matches = list(ENTRY.finditer(text))
    for index, match in enumerate(matches):
        if match.group("version") != version:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[match.end() : end].strip()
    known = ", ".join(m.group("version") for m in matches) or "none"
    raise SystemExit(
        f"{path} has no entry for {version}. Add one before releasing. "
        f"Entries found: {known}"
    )


def main() -> None:
    args = parse_args()
    body = BODY.format(
        version=args.version,
        korean=top_items(fontlog_entry(args.fontlog_ko, args.version), args.max_items),
        english=top_items(fontlog_entry(args.fontlog, args.version), args.max_items),
    )
    if args.output:
        args.output.write_text(body, encoding="utf-8")
        print(f"release notes: {args.output}")
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
