"""립싱크(입모양 ↔ 목소리) 자동 측정·보정 — 이 컴퓨터 안에서만 분석한다.

왜 필요한가
  화면 녹화 프로그램은 웹캠 영상과 마이크 소리를 따로 받아 합치기 때문에, 녹화 자체에서
  웹캠 영상이 소리보다 0.1~0.3초 늦게 담기는 경우가 흔하다 (3분50초 샘플: 입모양이 소리보다 약 0.27초 늦음 —
  말끝에서 소리는 끝났는데 입이 '…니다'를 계속 말하는 장면으로 확인).
  사람은 소리가 0.125초 이상 늦거나 0.045초 이상 이르면 어긋남을 알아챈다 (ITU-R BT.1359).

측정 방법
  1) 정리된 영상에서 얼굴(교수 카메라 창)을 찾는다 — 화면을 조각내 얼굴 인식 (MediaPipe Face Landmarker).
  2) 처음·가운데·끝 세 구간(각 60초)에서 프레임마다 '입 벌림'(윗입술↔아랫입술 / 얼굴 높이)을 잰다.
  3) 입 벌림과 소리 크기(로그 RMS)를 음절 리듬 대역(2~7Hz)만 남겨 맞대고, 상관이 가장 큰 시간차 = 어긋남.
     (느린 성분은 '말 전에 숨 들이쉬며 입 벌리기' 때문에 방향을 거꾸로 알려 준다 — 샘플에서 화면으로 확인)
     정점이 뚜렷하지 않으면(두 번째 정점의 1.3배 미만) 믿지 않는다. 구간별로 따로 재서 드리프트도 본다.
  4) 자연스러운 말에서도 입이 소리보다 약 20ms 먼저 움직이므로, 그만큼은 남기고 보정량을 정한다.
보정: 소리만 앞당기거나 늦춘다 (영상은 다시 인코딩하지 않음 · 화질 손실 없음).

필요: pip install mediapipe  +  python engine/setup_models.py lipsync  (얼굴 모델 3.7MB)
없으면 자동 측정은 건너뛰고, job.yaml 의 av_offset_ms 에 직접 숫자를 넣어 보정할 수 있다.
"""

from __future__ import annotations

import json
import subprocess

import numpy as np

from .util import MODELS, run

MODEL = MODELS / "face_landmarker.task"
NATURAL_LEAD_MS = 20      # 자연스러운 말에서 입이 소리보다 먼저 움직이는 정도
MIN_FIX_MS = 40           # 이보다 작은 어긋남은 사람이 못 느끼므로 보정하지 않음
WIN_SEC = 60.0
SCALE = 3                 # 작은 카메라 창 얼굴을 키워 인식


def unavailable() -> str | None:
    try:
        import mediapipe  # noqa: F401
    except Exception:  # noqa: BLE001
        return "mediapipe 가 없습니다 (pip install mediapipe)"
    if not MODEL.exists():
        return f"얼굴 모델이 없습니다: {MODEL} (python engine/setup_models.py lipsync)"
    return None


def _landmarker(video: bool):
    from mediapipe.tasks.python import BaseOptions, vision
    mode = vision.RunningMode.VIDEO if video else vision.RunningMode.IMAGE
    return vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(MODEL)), running_mode=mode, num_faces=1))


def _rgb(path, t: float, w: int, h: int, vf: str = "", n: int = 1):
    args = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path)]
    if n == 1:
        args += ["-frames:v", "1"]
    else:
        args += ["-t", f"{n:.3f}"]
    if vf:
        args += ["-vf", vf]
    p = subprocess.run(args + ["-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    k = len(p.stdout) // (w * h * 3)
    return np.frombuffer(p.stdout[: k * w * h * 3], np.uint8).reshape(k, h, w, 3)


def find_face(path, width: int, height: int, times: list[float]) -> dict | None:
    """화면을 겹치는 조각으로 나눠 얼굴을 찾는다 (작은 카메라 창 얼굴도 찾도록)."""
    import mediapipe as mp
    from PIL import Image
    lm = _landmarker(False)

    def pos(L, win):
        return sorted(set(list(range(0, max(1, L - win + 1), win // 2)) + [max(0, L - win)]))
    for t in times:
        img = _rgb(path, t, width, height)
        if not len(img):
            continue
        img = img[0]
        for win in (360, 540, min(width, height)):
            for y in pos(height, win):
                for x in pos(width, win):
                    tile = Image.fromarray(np.ascontiguousarray(img[y:y + win, x:x + win])).resize((720, 720))
                    r = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(np.array(tile))))
                    if r.face_landmarks:
                        L = r.face_landmarks[0]
                        xs, ys = [q.x for q in L], [q.y for q in L]
                        return {"x": x + min(xs) * win, "y": y + min(ys) * win,
                                "w": (max(xs) - min(xs)) * win, "h": (max(ys) - min(ys)) * win, "t": t}
    return None


def _crop_for(face: dict, width: int, height: int) -> tuple[int, int, int, int]:
    side = int(min(max(face["h"] * 3.6, 120), 480)) // 2 * 2
    cx, cy = face["x"] + face["w"] / 2, face["y"] + face["h"] / 2
    x = int(min(max(0, cx - side / 2), width - side)) // 2 * 2
    y = int(min(max(0, cy - side / 2), height - side)) // 2 * 2
    return side, side, x, y


def lip_series(path, crop, t0: float, dur: float):
    """구간 [t0, t0+dur) 의 프레임 시각과 입 벌림 값."""
    import mediapipe as mp
    w, h, x, y = crop
    W, H = w * SCALE, h * SCALE
    # 정리된 영상(clean.mp4)은 고정 프레임(30fps) → 프레임 번호로 시각을 정확히 계산 (구간 시작도 프레임 경계에 맞춤)
    q = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate",
                        "-of", "json", str(path)], capture_output=True)
    num, den = json.loads(q.stdout)["streams"][0]["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    k0 = int(round(t0 * fps))
    fr = _rgb(path, max(0.0, (k0 - 0.4) / fps), W, H, f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos", n=dur)
    n = len(fr)
    ts = [(k0 + i) / fps for i in range(n)]
    lm = _landmarker(True)
    vals = []
    for i in range(n):
        r = lm.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(fr[i])),
                                int(ts[i] * 1000) + i)
        if not r.face_landmarks:
            vals.append(np.nan)
            continue
        L = r.face_landmarks[0]
        vals.append(abs(L[14].y - L[13].y) / (abs(L[152].y - L[10].y) + 1e-6))
    return np.array(ts[:n]), np.array(vals)


def audio_env(path, t0: float, dur: float, rate: int = 100):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(path), "-vn",
                        "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True)
    x = np.frombuffer(p.stdout, "<i2").astype(np.float32) / 32768
    hop = 16000 // rate
    m = len(x) // hop
    env = np.sqrt((x[: m * hop].reshape(m, hop) ** 2).mean(1) + 1e-9)
    return t0 + np.arange(m) / rate, np.log(env + 1e-4)


def _band(x, rate: int, lo: float = 2.0, hi: float = 7.0):
    """음절 리듬(초당 2~7회)만 남긴다. 1Hz 아래 느린 성분에는 '말하기 전 숨 들이쉬며 입 벌리기' 같은
    습관이 섞여 입이 소리보다 먼저인 것처럼 잘못 보이게 만든다 (3분50초 샘플에서 확인)."""
    X = np.fft.rfft(x - x.mean())
    f = np.fft.rfftfreq(len(x), 1 / rate)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def best_lag(t_a, a, t_v, v, max_ms: int = 800, rate: int = 100) -> tuple[int, float, float]:
    """입(v)이 소리(a)보다 몇 ms 먼저 움직이는가 (+ = 입이 먼저 = 소리가 늦음 / - = 입이 늦음 = 소리가 이름).
    반환: (시간차, 상관, 정점 뚜렷함 = 최고 정점 / 두 번째 정점)."""
    ok = np.isfinite(v)
    t_v, v = t_v[ok], v[ok]
    if len(v) < 50:
        return 0, 0.0, 0.0
    t0, t1 = max(t_a[0], t_v[0]) + 1, min(t_a[-1], t_v[-1]) - 1
    if t1 - t0 < 10:
        return 0, 0.0, 0.0
    g = np.arange(t0, t1, 1 / rate)
    A, B = _band(np.interp(g, t_a, a), rate), _band(np.interp(g, t_v, v), rate)
    A, B = (A - A.mean()) / (A.std() + 1e-9), (B - B.mean()) / (B.std() + 1e-9)
    L = int(max_ms * rate / 1000)
    cs = [float(np.mean(A[k:] * B[: len(B) - k])) if k >= 0 else float(np.mean(A[:k] * B[-k:])) for k in range(-L, L + 1)]
    i = int(np.argmax(cs))
    w = int(0.12 * rate)                     # 최고 정점 ±120ms 밖의 다른 정점과 비교
    rest = [c for j, c in enumerate(cs) if abs(j - i) > w]
    second = max(rest) if rest else 0.0
    sharp = cs[i] / second if second > 1e-6 else 9.9
    return (i - L) * 1000 // rate, cs[i], round(sharp, 2)


def measure(path, duration: float, width: int, height: int, log=print) -> dict:
    why = unavailable()
    if why:
        return {"ok": False, "reason": why}
    mids = [duration * f for f in (0.15, 0.5, 0.85)] if duration > WIN_SEC * 2.5 else [duration / 2]
    face = find_face(path, width, height, mids + [min(5.0, duration / 3)])
    if not face:
        return {"ok": False, "reason": "화면에서 얼굴(교수 카메라 창)을 찾지 못했습니다"}
    crop = _crop_for(face, width, height)
    wins = []
    for m in mids:
        # 긴 영상은 세 구간(60초씩), 짧은 영상(2.5분 이하)은 전체를 한 구간으로 — 60초만으로는 근거가 부족하다
        dur = min(WIN_SEC, duration - 2) if len(mids) > 1 else max(10.0, duration - 2)
        t0 = max(0.0, min(m - dur / 2, duration - dur - 1))
        ts, v = lip_series(path, crop, t0, dur)
        ta, a = audio_env(path, t0, dur)
        lag, c, sharp = best_lag(ta, a, ts, v)
        found = float(np.isfinite(v).mean()) if len(v) else 0.0
        wins.append({"t0": round(t0, 1), "lag_ms": lag, "corr": round(c, 3), "sharp": sharp, "face_found": round(found, 2)})
        log(f"      립싱크 측정 {t0:6.0f}초~: 입이 소리보다 {lag:+d}ms "
            f"(상관 {c:.2f}, 정점 뚜렷함 {sharp:.1f}배, 얼굴 인식 {found:.0%})")
    good = [w for w in wins if w["corr"] >= 0.06 and w["sharp"] >= 1.3 and w["face_found"] >= 0.6]
    res = {"face": {k: round(v, 1) for k, v in face.items()}, "crop": crop, "windows": wins}
    if not good:
        return {**res, "ok": False, "reason": "입 움직임과 소리의 관계가 뚜렷하지 않아 자동 측정을 믿기 어렵습니다"}
    lags = [w["lag_ms"] for w in good]
    lag = int(np.median(lags))
    spread = max(lags) - min(lags)
    if len(good) >= 2 and spread > 120:
        return {**res, "ok": False, "lag_ms": lag, "spread_ms": spread,
                "reason": f"구간마다 어긋남이 다릅니다(차이 {spread}ms) — 녹화 중 싱크가 점점 벌어진 것으로 보여 자동 보정하지 않습니다"}
    fix = int(round((lag - NATURAL_LEAD_MS) / 10.0) * 10)
    return {**res, "ok": True, "lag_ms": lag, "spread_ms": spread, "fix_ms": fix if abs(fix) >= MIN_FIX_MS else 0}


def apply(src, dst, fix_ms: int, duration: float) -> None:
    """소리를 fix_ms 만큼 앞당긴다(+) 또는 늦춘다(-). 영상은 그대로 복사."""
    s = abs(fix_ms) / 1000.0
    af = (f"atrim=start={s:.3f},asetpts=PTS-STARTPTS,apad=pad_dur={s:.3f}" if fix_ms > 0
          else f"adelay={abs(fix_ms)}:all=1")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", af,
         "-c:a", "aac", "-b:a", "192k", "-t", f"{duration:.3f}", "-movflags", "+faststart", dst])
