#!/usr/bin/env bash
# 온담찬 로고 3안 생성 (gpt-image-2). 필요: OPENAI_API_KEY, api.openai.com 접근
set -euo pipefail
cd "$(dirname "$0")/.."
GEN=.claude/skills/homepage-builder-kr/scripts/gen-image.mjs
for v in A B C; do
  node "$GEN" --name "logo-$v" --n 2 --quality medium --size 1024x1024 \
    --out brand/logo/candidates --prompt-file "brand/prompts/logo-$v.txt"
done
