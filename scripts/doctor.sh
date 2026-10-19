#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
missing=0
for cmd in git node npm uv; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '%-6s %s\n' "$cmd" "$(command -v "$cmd")"
  else
    echo "MISSING: $cmd" >&2
    missing=1
  fi
done

if command -v node >/dev/null 2>&1; then
  # Iosevka declares engines.node >= 16, which is the floor. CI builds on 22,
  # so that is what is actually verified and what the docs recommend.
  node -e 'const major=Number(process.versions.node.split(".")[0]); if(major<16){console.error(`Node >=16 required by Iosevka; found ${process.versions.node}`); process.exit(1)} console.log(`node version ${process.versions.node}` + (major<22 ? " OK (22+ recommended; CI builds on 22)" : " OK"))'
fi

if command -v uv >/dev/null 2>&1; then
  uv --version

  # tools/font_utils.py stamps the version into every face; pyproject.toml
  # names the builder. A release tag is checked against the former, so catch
  # the two drifting apart here rather than at tag time.
  font_version="$(PYTHONPATH="$ROOT/tools" uv run python -c \
    'import font_utils; print(font_utils.PRESEVKA_VERSION)')"
  builder_version="$(sed -n 's/^version = "\(.*\)"$/\1/p' "$ROOT/pyproject.toml" | head -1)"
  if [[ "$font_version" != "$builder_version" ]]; then
    echo "MISSING: version sync — font_utils says $font_version, pyproject.toml says $builder_version" >&2
    missing=1
  else
    printf '%-6s %s\n' "version" "$font_version"
  fi
fi

# Workflow checks. actionlint is static and offline; the ref check resolves the
# tags the workflows name, which actionlint does not do and which otherwise
# only fails on GitHub, after the job has already been queued.
if command -v actionlint >/dev/null 2>&1; then
  if actionlint; then
    printf '%-6s %s\n' "lint" "workflows pass actionlint"
  else
    missing=1
  fi
else
  printf '%-6s %s\n' "lint" "actionlint not installed; skipping workflow lint"
fi

if command -v uv >/dev/null 2>&1; then
  uv run python "$ROOT/tools/check_workflows.py" || missing=1
fi

exit "$missing"
