#!/usr/bin/env bash
# 온담찬 사이트 사진 6장 일괄 생성 (gpt-image-2, 고품질 JPEG)
# 사용: OPENAI_API_KEY=sk-... bash ondamchan/generate-all.sh
set -euo pipefail
cd "$(dirname "$0")"
GEN=../gpt-image/generate.py
MODEL=${MODEL:-gpt-image-2}
QUALITY=${QUALITY:-high}

# 파일명 | 크기 | 사이트 자리
JOBS=(
  "01-dinner-set-hero|1536x1024|홈 '나를 위한 한 끼' · 1인 저녁세트 상세"
  "02-silver-dinner-tray|1024x1024|홈 '부모님께 전하는 한 끼' · 어르신 밥상"
  "03-doenjang-soup-closeup|1024x1024|상세페이지 국 클로즈업"
  "04-containers-topview|1536x1024|상세페이지 용기 탑뷰 (3:2)"
  "05-pickup-cabinet|1536x1024|픽업 안내"
  "06-shop-interior|1536x1024|가게 이야기 (16:9)"
)

mkdir -p photos
for job in "${JOBS[@]}"; do
  IFS='|' read -r name size place <<<"$job"
  if ls photos/"$name".* >/dev/null 2>&1; then echo "건너뜀(이미 있음): $name"; continue; fi
  echo "▶ $name ($size) — $place"
  python3 "$GEN" "$(cat prompts/"$name".txt)" --model "$MODEL" --size "$size" \
    --quality "$QUALITY" --format jpeg -o "tmp-$name"
  mv "tmp-$name"/*.jpeg "photos/$name.jpg" && rmdir "tmp-$name"
done
echo "완료: $(ls photos | wc -l)장 → ondamchan/photos/"
