#!/usr/bin/env python3
"""강의 후반작업 도구 — 사용법
  ls_cli.py new <작업ID>                  새 작업 폴더·작업서 만들기
  ls_cli.py run <작업ID> [--from 단계] [--only 단계] [--force]
  ls_cli.py status <작업ID>
단계: ingest clean asr text study outputs print
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ls import job as jobmod  # noqa: E402
from ls import pipeline  # noqa: E402
from ls.util import need_tools, read_json  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("new").add_argument("id")
    r = sub.add_parser("run")
    r.add_argument("id")
    r.add_argument("--from", dest="start", choices=pipeline.NAMES)
    r.add_argument("--only", choices=pipeline.NAMES)
    r.add_argument("--force", action="store_true")
    sub.add_parser("status").add_argument("id")
    a = ap.parse_args()
    need_tools()
    if a.cmd == "new":
        d = jobmod.create(a.id)
        print(f"만들었습니다: {d}\n  1) {d/'input'} 에 영상을 넣고  2) {d/'job.yaml'} 을 채운 뒤  3) ls_cli.py run {a.id}")
        return
    try:
        job = jobmod.load(a.id, need_consent=(a.cmd == "run"))
    except jobmod.JobError as e:
        raise SystemExit(str(e))
    if a.cmd == "status":
        for n in pipeline.NAMES:
            d = read_json(job.work / f"{n}.json")
            print(f"{pipeline.LABEL[n]}  {'완료 · ' + d.get('_summary', '') if d else '아직'}")
        return
    pipeline.run(job, start=a.start, only=a.only, force=a.force)
    print(f"\n끝났습니다 → {job.out}")


if __name__ == "__main__":
    main()
