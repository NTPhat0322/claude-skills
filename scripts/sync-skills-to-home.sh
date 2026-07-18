#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CLAUDE_USER_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"
rsync -a "$ROOT/.claude/skills/" "$DEST/"
echo "Merged .claude/skills/ from $ROOT into $DEST"
