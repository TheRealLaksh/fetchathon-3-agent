"""Concatenate scene clips into demo.mp4 (1920x1080, 30 fps, H.264 + AAC), burn in captions, write captions.srt and voiceover.txt.
Run from video-output:  python tools/build_final.py
Pace: every scene is played 1.04x (video and audio together) to land inside the 5:00 limit; scene audio files in audio/ stay at normal speed.
"""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SPEED = 1.04
LEAD = 0.35
SCENES = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]
OFFSET = {"05": 3.0}  # narration starts 3 s into scene 05


def dur(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.decode().strip())


def chunks(text):
    parts = []
    for sent in re.split(r"(?<=[.?!])\s+", text.strip()):
        if len(sent) <= 95:
            parts.append(sent)
            continue
        pieces, cur = [], ""
        for w in sent.split(" "):
            if len(cur) + len(w) + 1 > 90 and (cur.endswith(",") or cur.endswith(":") or len(cur) > 70):
                pieces.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            pieces.append(cur)
        parts += pieces
    return parts


def ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


srt, vo, scene_info = [], [], []
t0, idx = 0.0, 1
for n in SCENES:
    text = open(f"narration/scene{n}.txt", encoding="utf-8").read().strip()
    a = dur(f"audio/scene{n}.wav")
    off = OFFSET.get(n, 0.0)
    clip = f"clips/scene{n}.mp4"
    cdur = dur(clip)
    use = min(cdur, off + a + LEAD)
    cs = chunks(text)
    total_chars = sum(len(c) for c in cs)
    cum = 0
    for c in cs:
        s = t0 + (off + a * cum / total_chars) / SPEED
        cum += len(c)
        e = t0 + (off + a * cum / total_chars) / SPEED
        srt.append(f"{idx}\n{ts(s)} --> {ts(e - 0.05)}\n{c}\n")
        idx += 1
    vo.append(f"Scene {int(n)}\n{text}\n")
    scene_info.append((n, t0, use / SPEED))
    t0 += use / SPEED

open("captions.srt", "w", encoding="utf-8").write("\n".join(srt))
open("voiceover.txt", "w", encoding="utf-8").write("\n".join(vo))
print("total", round(t0, 2), "s")

inputs, vf, af, cat = [], [], [], ""
for i, (n, st, d) in enumerate(scene_info):
    use = d * SPEED
    inputs += ["-i", f"clips/scene{n}.mp4"]
    vf.append(f"[{i}:v]trim=0:{use:.3f},setpts=(PTS-STARTPTS)/{SPEED},fps=30,format=yuv420p[v{i}]")
    af.append(f"[{i}:a]atrim=0:{use:.3f},asetpts=PTS-STARTPTS,atempo={SPEED}[a{i}]")
    cat += f"[v{i}][a{i}]"
style = "FontName=Segoe UI Semibold,FontSize=7.6,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,BorderStyle=1,Outline=0.8,Shadow=0,Alignment=2,MarginV=4,MarginL=40,MarginR=40"  # libass units: PlayRes 384x288, scaled x3.75 to 1080p
g = ";".join(vf + af) + f";{cat}concat=n={len(scene_info)}:v=1:a=1[vc][ac];[vc]subtitles=captions.srt:force_style='{style}'[v];[ac]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + inputs + ["-filter_complex", g, "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
       "-movflags", "+faststart", "demo.mp4"]
subprocess.run(cmd, check=True)
print("demo.mp4", round(dur("demo.mp4"), 2), "s")
with open("scene_times.txt", "w") as f:
    for n, st, d in scene_info:
        f.write(f"{n} {st:.2f} {st + d:.2f}\n")
