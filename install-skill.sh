#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.claude/skills/scalify-cli"
SKILL_URL="https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/skills/scalify-cli/SKILL.md"

echo "Installing Scalify CLI skill for Claude Code..."

mkdir -p "$SKILL_DIR"
curl -fsSL "$SKILL_URL" -o "$SKILL_DIR/SKILL.md"

echo "Skill installed to $SKILL_DIR/SKILL.md"
echo "Restart Claude Code (or start a new session) for the skill to take effect."
