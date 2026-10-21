"""GPT 이미지 일괄 생성 스크립트.

사용 예)
  export OPENAI_API_KEY=sk-...
  python generate.py "공원에서 스트레칭하는 시니어 부부, 수채화 스타일"
  python generate.py -f prompts.txt --size 1024x1536 --quality high
  python generate.py "이 사진에 로고 추가" --image photo.png --image logo.png
"""

import argparse
import base64
import os
import sys
from datetime import datetime
from pathlib import Path

from openai import OpenAI


def parse_args():
    p = argparse.ArgumentParser(description="OpenAI gpt-image 이미지 생성")
    p.add_argument("prompt", nargs="?", help="프롬프트 (또는 -f 로 파일 지정)")
    p.add_argument("-f", "--file", help="한 줄에 프롬프트 하나씩 적은 텍스트 파일")
    p.add_argument("--image", action="append", default=[], help="참고 이미지 (편집 모드, 여러 번 지정 가능)")
    p.add_argument("--model", default="gpt-image-1")
    p.add_argument("--size", default="1024x1024", choices=["1024x1024", "1024x1536", "1536x1024", "auto"])
    p.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto"])
    p.add_argument("--background", default="auto", choices=["auto", "opaque", "transparent"])
    p.add_argument("--format", default="png", choices=["png", "jpeg", "webp"])
    p.add_argument("-n", type=int, default=1, help="프롬프트당 생성 장수 (1~10)")
    p.add_argument("-o", "--out", default="output", help="저장 폴더")
    return p.parse_args()


def load_prompts(args):
    if args.file:
        lines = Path(args.file).read_text(encoding="utf-8").splitlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    if args.prompt:
        return [args.prompt]
    sys.exit("프롬프트를 입력하거나 -f 로 파일을 지정하세요.")


def generate(client, prompt, args):
    params = dict(
        model=args.model, prompt=prompt, n=args.n, size=args.size,
        quality=args.quality, background=args.background, output_format=args.format,
    )
    if args.image:
        files = [open(path, "rb") for path in args.image]
        try:
            return client.images.edit(image=files, **params)
        finally:
            for f in files:
                f.close()
    return client.images.generate(**params)


def main():
    args = parse_args()
    if args.background == "transparent" and args.format == "jpeg":
        sys.exit("투명 배경은 png 또는 webp 형식에서만 가능합니다.")
    prompts = load_prompts(args)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    client = OpenAI()  # OPENAI_API_KEY 환경변수 사용

    for idx, prompt in enumerate(prompts, 1):
        print(f"[{idx}/{len(prompts)}] 생성 중: {prompt[:50]}...")
        result = generate(client, prompt, args)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        for i, item in enumerate(result.data, 1):
            path = out_dir / f"{stamp}-p{idx}-{i}.{args.format}"
            path.write_bytes(base64.b64decode(item.b64_json))
            print(f"  저장: {path}")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY 환경변수를 먼저 설정하세요.")
    main()
