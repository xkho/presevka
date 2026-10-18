from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# actionlint is a static checker and never asks GitHub whether a tag exists, so
# a typo like astral-sh/setup-uv@v10 passes it and then fails the job before any
# step runs. This resolves every ref the workflows actually name.
USES = re.compile(r"^\s*(?:-\s*)?uses:\s*['\"]?([^'\"\s#]+)", re.MULTILINE)

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
CACHE = ROOT / ".cache" / "workflow-refs.json"


def refs() -> set[str]:
    found: set[str] = set()
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        for ref in USES.findall(path.read_text(encoding="utf-8")):
            # Local and container actions are not published tags.
            if ref.startswith((".", "docker://")) or "@" not in ref:
                continue
            found.add(ref)
    return found


def load_cache() -> set[str]:
    try:
        return set(json.loads(CACHE.read_text()))
    except Exception:
        return set()


def exists(repo: str, tag: str) -> bool | None:
    """True/False if resolved, None if GitHub could not be reached."""
    url = f"https://api.github.com/repos/{repo}/git/ref/tags/{tag}"
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{repo}/git/ref/tags/{tag}"],
            capture_output=True, timeout=20,
        )
        if out.returncode == 0:
            return True
        if b"Not Found" in out.stderr or b"404" in out.stderr:
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    try:
        urllib.request.urlopen(url, timeout=20)
        return True
    except urllib.error.HTTPError as err:
        return False if err.code == 404 else None
    except Exception:
        return None


def main() -> int:
    wanted = refs()
    if not wanted:
        print("no workflow actions to check")
        return 0

    verified = load_cache()
    bad: list[str] = []
    skipped: list[str] = []
    for ref in sorted(wanted):
        if ref in verified:
            continue
        repo, tag = ref.rsplit("@", 1)
        result = exists(repo, tag)
        if result is True:
            verified.add(ref)
        elif result is False:
            bad.append(ref)
        else:
            skipped.append(ref)

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(sorted(verified), indent=2) + "\n")

    if bad:
        print("workflow actions that do not resolve:", file=sys.stderr)
        for ref in bad:
            repo, tag = ref.rsplit("@", 1)
            print(f"  {ref}  (no tag {tag} in {repo})", file=sys.stderr)
        print("A job using these fails at 'Set up job'.", file=sys.stderr)
        return 1
    if skipped:
        print(f"workflow actions: {len(wanted) - len(skipped)} ok, "
              f"{len(skipped)} unchecked (GitHub unreachable)")
        return 0
    print(f"workflow actions: all {len(wanted)} refs resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
