"""자막 파일(SRT·VTT·ASS) 만들기."""

from __future__ import annotations


def _t(sec: float, sep: str) -> str:
    ms = int(round(sec * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"


def srt(cues: list[dict], key: str) -> str:
    n, out = 0, []
    for c in cues:
        if not c.get(key):
            continue
        n += 1
        out.append(f"{n}\n{_t(c['start'], ',')} --> {_t(c['end'], ',')}\n{c[key]}\n")
    return "\n".join(out)


def vtt(cues: list[dict], key: str) -> str:
    out = ["WEBVTT\n"]
    for c in cues:
        if c.get(key):
            out.append(f"{_t(c['start'], '.')} --> {_t(c['end'], '.')}\n{c[key]}\n")
    return "\n".join(out)


def ass(cues: list[dict], key: str, size: int, margin_v: int = 58) -> str:
    def at(sec):
        cs = int(round(sec * 100))
        return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Pretendard,{size},&H00FFFFFF,&H000000FF,&HC8000000,&H96000000,-1,0,0,0,100,100,0,0,3,10,0,2,120,120,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f"Dialogue: 0,{at(c['start'])},{at(c['end'])},Sub,,0,0,0,,{c[key].replace(chr(10), chr(92) + 'N')}"
             for c in cues if c.get(key)]
    return head + "\n".join(lines) + "\n"
