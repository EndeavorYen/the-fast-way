#!/usr/bin/env bash
set -euo pipefail

platform="${1:-all}"
skip_leaves=0
if [[ "${THE_FAST_WAY_SKIP_LEAVES:-}" == "1" ]]; then
  skip_leaves=1
fi
if [[ "${2:-}" == "--skip-leaves" ]]; then
  skip_leaves=1
fi

case "$platform" in
  grok|claude|cursor|hermes|all) ;;
  *)
    echo "usage: $0 [grok|claude|cursor|hermes|all] [--skip-leaves]" >&2
    exit 2
    ;;
esac

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
skill_src="$repo_root/SKILL.md"
readme_src="$repo_root/README.md"
refs_src="$repo_root/references"
if [[ ! -f "$skill_src" ]]; then
    echo "SKILL.md not found at $skill_src" >&2
    exit 1
fi

dest_for() {
  local name="$1"
  local home="${HOME}"
  case "$name" in
    grok)
      local root="${GROK_HOME:-$home/.grok}"
      printf '%s\n' "$root/skills/the-fast-way"
      ;;
    hermes)
      local root="${HERMES_HOME:-$home/.hermes}"
      printf '%s\n' "$root/skills/the-fast-way"
      ;;
    claude) printf '%s\n' "$home/.claude/skills/the-fast-way" ;;
    cursor) printf '%s\n' "$home/.cursor/skills/the-fast-way" ;;
    *)
      echo "Unknown platform $name" >&2
      return 1
      ;;
  esac
}

install_to() {
  local name="$1"
  local dest
  dest="$(dest_for "$name")"
  mkdir -p "$dest"
  cp "$skill_src" "$dest/SKILL.md"
  if [[ -f "$readme_src" ]]; then
    cp "$readme_src" "$dest/README.md"
  fi
  if [[ -d "$refs_src" ]]; then
    rm -rf "$dest/references"
    cp -R "$refs_src" "$dest/references"
  fi
  echo "Installed $name -> $dest"
}

install_leaves() {
  local leaf_platform="$1"
  if ! command -v git >/dev/null 2>&1; then
    echo "git is required to install leaf skills from GitHub" >&2
    exit 1
  fi
  local tmp_root
  tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/the-fast-way-leaves.XXXXXX")"
  # shellcheck disable=SC2064
  trap 'rm -rf "$tmp_root"' RETURN
  local url name clone_dest installer
  for spec in \
    "gentle-grill-me|https://github.com/EndeavorYen/gentle-grill-me.git" \
    "musk-algorithm-skill|https://github.com/EndeavorYen/musk-algorithm-skill.git" \
    "just-ten-more|https://github.com/EndeavorYen/just-ten-more.git"
  do
    name="${spec%%|*}"
    url="${spec#*|}"
    clone_dest="$tmp_root/$name"
    echo "Cloning $url"
    git clone --depth 1 "$url" "$clone_dest"
    installer="$clone_dest/scripts/install.sh"
    if [[ ! -f "$installer" ]]; then
      echo "missing scripts/install.sh in $name" >&2
      exit 1
    fi
    echo "Installing leaf $name for $leaf_platform"
    if ! bash "$installer" "$leaf_platform"; then
      if [[ "$leaf_platform" == "hermes" ]]; then
        echo "Skip $name on hermes: leaf installer rejected the platform"
        continue
      fi
      echo "leaf install failed: $name $leaf_platform" >&2
      exit 1
    fi
  done
}

if [[ "$platform" == "all" ]]; then
  for t in grok claude cursor hermes; do
    install_to "$t"
  done
else
  install_to "$platform"
fi
if [[ "$skip_leaves" -eq 0 ]]; then
  install_leaves "$platform"
fi
