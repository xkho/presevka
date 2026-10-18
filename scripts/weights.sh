#!/usr/bin/env bash

# Canonical static-weight order shared by every build stage.
readonly PRESEVKA_WEIGHTS=(
  Thin
  ExtraLight
  Light
  Regular
  Medium
  SemiBold
  Bold
  ExtraBold
  Black
)

declare -Ar PRESEVKA_WEIGHT_CLASSES=(
  [Thin]=100
  [ExtraLight]=200
  [Light]=300
  [Regular]=400
  [Medium]=500
  [SemiBold]=600
  [Bold]=700
  [ExtraBold]=800
  [Black]=900
)

# Upright and true Iosevka Italic faces. Pretendard Hangul remains upright in
# both faces because the upstream font does not provide an italic design.
readonly PRESEVKA_SLOPES=(
  Upright
  Italic
)

presevka_variant_suffix() {
  local weight="$1"
  local slope="$2"

  if [[ "$slope" == "Upright" ]]; then
    printf '%s\n' "$weight"
  elif [[ "$weight" == "Regular" ]]; then
    printf '%s\n' "$slope"
  else
    printf '%s%s\n' "$weight" "$slope"
  fi
}

# Hinting stage, selected by PRESEVKA_HINT and shared by build_iosevka.sh,
# merge.sh and the QA step.
#   full  - ttfautohint over the merged font, so Hangul is hinted too (default)
#   latin - ttfautohint over the Iosevka base only, leaving Hangul unhinted
#   gasp  - no ttfautohint; only the gasp smoothing and dropout-control table
#   none  - ship raw outlines
presevka_hint_mode() {
  local mode="${PRESEVKA_HINT:-full}"
  case "$mode" in
    full | latin | gasp | none)
      printf '%s\n' "$mode"
      ;;
    *)
      echo "PRESEVKA_HINT must be one of: full latin gasp none (got '$mode')" >&2
      return 1
      ;;
  esac
}

# Replace a built font with its hinted form. Writes through a temporary file so
# an interrupted run cannot leave a half-written face behind.
presevka_apply_hinting() {
  local root="$1" action="$2" font="$3"
  uv run python "$root/tools/hint_font.py" "$action" \
    --input "$font" --output "$font.tmp"
  mv "$font.tmp" "$font"
}

# Latin character-variant preset, selected by PRESEVKA_PRESET. "stock" uses
# Iosevka's own glyph designs; any other value names a fragment in
# config/presets/ that is appended to the base build plan.
presevka_preset() {
  local preset="${PRESEVKA_PRESET:-stock}"
  # Restricted to a plain name so the value cannot escape config/presets/.
  if [[ ! "$preset" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
    echo "PRESEVKA_PRESET must match [a-z0-9-]; got '$preset'" >&2
    return 1
  fi
  printf '%s\n' "$preset"
}

# Write the build plan Iosevka will use: the base grid, plus the preset's
# character variants when one is selected.
presevka_write_build_plan() {
  local root="$1" preset="$2" dest="$3"
  cp "$root/config/private-build-plans.toml" "$dest"
  [[ "$preset" == "stock" ]] && return 0

  local fragment="$root/config/presets/$preset.toml"
  if [[ ! -f "$fragment" ]]; then
    echo "Unknown PRESEVKA_PRESET '$preset'. Available:" >&2
    local found=0
    for file in "$root"/config/presets/*.toml; do
      [[ -e "$file" ]] || continue
      found=1
      printf '  %s\n' "$(basename "$file" .toml)" >&2
    done
    (( found )) || echo "  (none)" >&2
    echo "  stock" >&2
    return 1
  fi
  printf '\n' >>"$dest"
  cat "$fragment" >>"$dest"
}
