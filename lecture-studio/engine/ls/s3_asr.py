"""③ 받아쓰기 — 이 컴퓨터 안에서만 (영상·음성을 외부로 보내지 않는다).

백엔드(job.yaml 의 asr.backend):
  sherpa-whisper  GitHub 에서 받는 ONNX Whisper + Silero VAD. 말 구간 단위 시각. (클라우드·인터넷 제한 환경에서도 동작)
  faster-whisper  Hugging Face 모델. 단어 단위 시각 → 자막 싱크가 가장 정확. (PC 권장, 모델 내려받기 필요)
  words-file      input/<영상파일명>.words.json  [{start,end,text}, …] 를 그대로 사용 (미리 받아쓴 경우)

결과: work/asr.json  {"backend", "segments":[{start,end,text,words?}]}
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

from .job import Job
from .util import MODELS, StageError, read_json, run


def _wav16k(src: Path, dst: Path) -> np.ndarray:
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", dst])
    with wave.open(str(dst), "rb") as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
    return pcm.astype(np.float32) / 32768.0


def _sherpa(job: Job, audio: np.ndarray, log) -> list[dict]:
    try:
        import sherpa_onnx
    except ImportError as e:
        raise StageError("sherpa-onnx 가 없습니다 → pip install sherpa-onnx") from e
    model = (job.get("asr") or {}).get("model", "medium")
    mdir = MODELS / f"whisper-{model}"
    enc, dec, tok = mdir / f"{model}-encoder.int8.onnx", mdir / f"{model}-decoder.int8.onnx", mdir / f"{model}-tokens.txt"
    vad_model = MODELS / "silero_vad.onnx"
    for p in (enc, dec, tok, vad_model):
        if not p.exists():
            raise StageError(f"받아쓰기 모델이 없습니다: {p}\n  → README 의 '받아쓰기 모델 내려받기'를 따라 주세요.")
    lang = job.get("source_language", "ko")
    recognizer = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(enc), decoder=str(dec), tokens=str(tok), language=lang, task="transcribe", num_threads=4,
        tail_paddings=2000)   # 문장 끝이 잘리지 않도록 뒤에 무음을 덧붙여 디코딩

    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = str(vad_model)
    cfg.silero_vad.threshold = 0.5
    cfg.silero_vad.min_silence_duration = 0.45    # 이만큼 쉬면 말 구간을 끊는다 (숨 쉬는 틈)
    cfg.silero_vad.min_speech_duration = 0.25
    cfg.silero_vad.max_speech_duration = 12.0     # 긴 구간은 Whisper 가 중간을 빠뜨리므로 짧게
    cfg.sample_rate = 16000
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=120)

    segments, win = [], cfg.silero_vad.window_size
    pad_front, pad_back = int(0.30 * 16000), int(1.00 * 16000)   # VAD 가 말끝을 일찍 자르는 것을 막는 여유

    def drain():
        while not vad.empty():
            seg = vad.front
            s0, n = int(seg.start), len(seg.samples)
            vad.pop()
            if n < 16000 * 0.3:
                continue
            a, b = max(0, s0 - pad_front), min(len(audio), s0 + n + pad_back)
            samples = audio[a:b]
            start = s0 / 16000.0
            stream = recognizer.create_stream()
            stream.accept_waveform(16000, samples)
            recognizer.decode_stream(stream)
            text = stream.result.text.strip()
            end = start + n / 16000.0
            if text:
                segments.append({"start": round(start, 3), "end": round(end, 3), "text": text})
                log(f"      {start:6.1f}–{end:6.1f}s  {text[:60]}")

    for i in range(0, len(audio), win):
        vad.accept_waveform(audio[i:i + win])
        drain()
    vad.flush()
    drain()
    return segments


def _faster_whisper(job: Job, audio_path: Path, log) -> list[dict]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise StageError("faster-whisper 가 없습니다 → pip install faster-whisper (모델은 처음 한 번 내려받습니다)") from e
    model_name = (job.get("asr") or {}).get("model", "medium")
    model = None
    for dev, ct in (("cuda", "float16"), ("cpu", "int8")):
        try:
            model = WhisperModel(model_name, device=dev, compute_type=ct)
            break
        except Exception:  # noqa: BLE001 — GPU 가 없으면 CPU 로
            continue
    if model is None:
        raise StageError("faster-whisper 모델을 불러오지 못했습니다 (인터넷 연결·huggingface.co 접근 확인)")
    segs, _info = model.transcribe(str(audio_path), language=job.get("source_language", "ko"), word_timestamps=True,
                                   vad_filter=True)
    out = []
    for s in segs:
        words = [{"start": round(w.start, 3), "end": round(w.end, 3), "text": w.word.strip()} for w in (s.words or [])]
        out.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": words})
    return out


def _words_file(job: Job) -> list[dict]:
    p = job.input / f"{job.video.name}.words.json"
    words = read_json(p)
    if not words:
        raise StageError(f"받아쓴 글 파일이 없습니다: {p}")
    segs, cur = [], []
    for w in words:  # 0.6초 이상 쉬면 새 구간
        if cur and w["start"] - cur[-1]["end"] >= 0.6:
            segs.append(cur)
            cur = []
        cur.append(w)
    segs.append(cur)
    return [{"start": s[0]["start"], "end": s[-1]["end"], "text": " ".join(w["text"] for w in s), "words": s} for s in segs]


def run_stage(job: Job, log=print) -> dict:
    backend = (job.get("asr") or {}).get("backend", "sherpa-whisper")
    wav = job.work / "audio16k.wav"
    audio = _wav16k(job.work / "clean.mp4", wav)
    log(f"      받아쓰기 방식: {backend} (영상·음성은 외부로 나가지 않습니다)")
    if backend == "sherpa-whisper":
        segments = _sherpa(job, audio, log)
    elif backend == "faster-whisper":
        segments = _faster_whisper(job, wav, log)
    elif backend == "words-file":
        segments = _words_file(job)
    else:
        raise StageError(f"알 수 없는 받아쓰기 방식: {backend}")
    if not segments:
        raise StageError("말소리를 찾지 못했습니다 (무음이거나 소리가 너무 작습니다)")
    chars = sum(len(s["text"]) for s in segments)
    return {"backend": backend, "segments": segments,
            "_summary": f"말 구간 {len(segments)}개 · {chars}자 ({backend})"}
