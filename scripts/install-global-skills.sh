#!/usr/bin/env bash
# Install this repo's Claude Code skills as global (user-level) skills: ~/.claude/skills/<name>
# Usage: ./scripts/install-global-skills.sh            # install all skills in .claude/skills
#        ./scripts/install-global-skills.sh homepage-builder-kr
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$repo_root/.claude/skills"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

mkdir -p "$dest"
names=("$@")
if [ ${#names[@]} -eq 0 ]; then
  for d in "$src"/*/; do names+=("$(basename "$d")"); done
fi

for name in "${names[@]}"; do
  if [ ! -f "$src/$name/SKILL.md" ]; then
    echo "skip: $name (SKILL.md 없음)" >&2
    continue
  fi
  rm -rf "${dest:?}/$name"
  cp -R "$src/$name" "$dest/$name"
  echo "installed: $dest/$name"
done

echo "완료 — Claude Code를 다시 열면 /homepage-builder-kr 로 사용할 수 있습니다."
