#!/bin/bash
# HY FLIP GPT 실사 이미지 원클릭 파이프라인
#   bash scripts/images_pipeline.sh --figma            # Figma 로 이미 만든 사진 받기 → 로고 목업 합성 → 갤러리 → 스크린샷
#   bash scripts/images_pipeline.sh                    # (OpenAI 직결) 진단 → 생성 → 갤러리 → 스크린샷
#   ... --commit                                       # + main 에 커밋·푸시 (두 모드 모두)
# 이미 있는 사진은 건너뛰므로 여러 번 실행해도 비용이 중복되지 않습니다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
COMMIT=0; FIGMA=0
for a in "$@"; do
  case "$a" in
    --commit) COMMIT=1 ;;
    --figma) FIGMA=1 ;;
    *) echo "알 수 없는 옵션: $a"; exit 1 ;;
  esac
done

step() { printf '\n━━ %s\n' "$1"; }

if [ "$FIGMA" = 1 ]; then
  step "1/5 Figma 원본 접속 진단"
  python3 scripts/fetch_figma.py --check || exit 2

  step "2/5 원본 내려받기 (없는 것만)"
  python3 scripts/fetch_figma.py
  GEN=$?

  step "3/5 로고 목업 합성 (빈 배경 + 확정 로고)"
  python3 scripts/composite_mockups.py || GEN=1
else
  step "1/5 키·네트워크 진단"
  python3 scripts/gen_image.py --check || exit 2

  step "2/5 로고 참고 이미지 확인 (목업용)"
  if [ ! -f logo/png/logo-D.png ] || [ ! -f logo/png/logo-A.png ]; then
    node scripts/shoot.mjs --logos || exit 1
  else
    echo "✓ logo/png 준비됨"
  fi

  step "3/5 GPT 이미지 생성 (없는 것만)"
  python3 scripts/gen_image.py --all
  GEN=$?
fi

step "4/5 갤러리 + 스크린샷"
python3 scripts/build_gallery.py
node scripts/shoot.mjs detail/detail-final.html home/home-final.html assets/gallery.html logo/logo-board-r2.html

if [ "$COMMIT" = 1 ]; then
  step "5/5 커밋·푸시"
  REPO="$(git rev-parse --show-toplevel)"
  git -C "$REPO" add "$ROOT/assets" "$ROOT/shots" "$ROOT/logo/png"
  if git -C "$REPO" diff --cached --quiet; then
    echo "변경 없음 — 커밋 생략"
  else
    N=$(ls "$ROOT"/assets/*.png 2>/dev/null | wc -l)
    git -C "$REPO" commit -q -m "HY FLIP: GPT photoreal images ($N) and refreshed screenshots" \
      && for i in 0 2 4 8 16; do sleep "$i"; git -C "$REPO" push -q origin HEAD:main && break; done
    git -C "$REPO" log --oneline -1
  fi
else
  step "5/5 커밋 생략 (--commit 을 붙이면 저장까지 합니다)"
fi

[ "$GEN" = 0 ] && echo "✓ 파이프라인 완료" || { echo "⚠ 일부 이미지 실패 — 위 안내를 확인하세요"; exit 1; }
