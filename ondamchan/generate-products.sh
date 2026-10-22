#!/usr/bin/env bash
# 반찬 상품 사진 일괄 생성 (prompts/products/<slug>.txt → photos/products/<slug>.jpg)
# 정사각 1024, gpt-image-2 고품질. 동시에 5장씩 만들고 이미 있는 사진은 건너뛴다.
# 사용: OPENAI_API_KEY=sk-... bash ondamchan/generate-products.sh
set -euo pipefail
cd "$(dirname "$0")"
export MODEL=${MODEL:-gpt-image-2} QUALITY=${QUALITY:-high}
mkdir -p photos/products

one() {
  local slug=$1 out=photos/products/$1.jpg tmp
  [ -f "$out" ] && { echo "건너뜀(이미 있음): $slug"; return; }
  tmp=$(mktemp -d)
  python3 ../gpt-image/generate.py "$(cat "prompts/products/$slug.txt")" --model "$MODEL" \
    --size 1024x1024 --quality "$QUALITY" --format jpeg -o "$tmp" >/dev/null
  mv "$tmp"/*.jpeg "$out" && rmdir "$tmp" && echo "완료: $slug"
}
export -f one
ls prompts/products | sed 's/\.txt$//' | xargs -P 5 -I{} bash -c 'one {}'
echo "상품 사진 $(ls photos/products | wc -l)장 → ondamchan/photos/products/"
