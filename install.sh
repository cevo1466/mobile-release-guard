#!/usr/bin/env bash
# One-command installer for the mobile-release-guard Claude Code skill.
# Usage: curl -fsSL https://raw.githubusercontent.com/cevo1466/mobile-release-guard/main/install.sh | bash
set -euo pipefail

REPO="cevo1466/mobile-release-guard"
REF="${MRG_REF:-main}"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/mobile-release-guard"

command -v curl >/dev/null || { echo "curl is required" >&2; exit 1; }
command -v tar  >/dev/null || { echo "tar is required"  >&2; exit 1; }

tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$REF.tar.gz" | tar -xz -C "$tmp"
src="$(find "$tmp" -maxdepth 3 -type d -path '*/skills/mobile-release-guard' | head -1)"
[ -f "$src/SKILL.md" ] || { echo "SKILL.md not found in download" >&2; exit 1; }

mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ]; then
  bak="$DEST.bak.$(date +%Y%m%d%H%M%S)"
  mv "$DEST" "$bak"; echo "Existing install moved to $bak"
fi
cp -r "$src" "$DEST"
chmod +x "$DEST"/scripts/*.sh 2>/dev/null || true
echo "Installed to $DEST"
echo "Restart Claude Code, then run: /mobile-release-guard"
