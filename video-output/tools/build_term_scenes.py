"""Builds scenes 05, 06, 08, 09 (terminal + code segments) from the raw captures.
Run from video-output:  python tools/build_term_scenes.py
Terminal waits are sped up 8x and labelled on screen; everything else is real time.
"""
import subprocess, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(ROOT, "clips")
AUDIO = os.path.join(ROOT, "audio")
FONT = "fontfile='C\\:/Windows/Fonts/segoeui.ttf'"
MASK = "drawbox=x=0:y=93:w=1920:h=62:color=0x1e1e1e:t=fill"
LEAD = 0.35


def dur(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.decode().strip())


def label(text, enable=None):
    en = f":enable='{enable}'" if enable else ""
    return f"drawtext={FONT}:text='{text}':x=(w-text_w)/2:y=8:fontsize=26:fontcolor=white:box=1:boxcolor=0x000000@0.75:boxborderw=8{en}"


def seg(idx, start, end, speed=1.0, mask=False, labels=(), hold_to=None, tag="v"):
    f = f"[{idx}:v]trim=start={start}:end={end},setpts=(PTS-STARTPTS)/{speed},scale=1920:1080:flags=lanczos,fps=30"
    if hold_to:
        f += f",tpad=stop_mode=clone:stop_duration={hold_to}"
    if mask:
        f += "," + MASK
    for l in labels:
        f += "," + l
    return f + f"[{tag}]"


def run(scene, inputs, graph, vout, total, audio_delay=0.0):
    wav = os.path.join(AUDIO, f"scene{scene}.wav")
    inputs = inputs + [wav]
    ai = len(inputs) - 1
    delay = f"adelay={int(audio_delay*1000)}|{int(audio_delay*1000)}," if audio_delay else ""
    g = ";".join(graph) + f";[{ai}:a]{delay}apad=pad_dur=3,atrim=0:{total:.3f}[a]"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for i in inputs:
        cmd += ["-i", i]
    out = os.path.join(CLIPS, f"scene{scene}.mp4")
    cmd += ["-filter_complex", g, "-map", f"[{vout}]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "1", out]
    subprocess.run(cmd, check=True)
    print(scene, round(dur(out), 2), "s")


T = lambda n: os.path.join(CLIPS, f"rawT{n}.mp4")
RAW9B = os.path.join(CLIPS, "raw09b.mp4")
A = lambda n: dur(os.path.join(AUDIO, f"scene{n}.wav"))
SPED = "local test client, same agent, sped up 8x"
SAME = "local test client, same agent"

# scene 05: sped run, then hold the finished answer; narration starts 3 s in
total = 3 + A("05") + LEAD
sp = (57.0 - 3.0) / 8
run("05", [T("05")], [
    seg(0, 3.0, 57.0, 8, labels=[label(SPED, f"between(t,0,{sp:.2f})"), label(SAME, f"gt(t,{sp:.2f})")], hold_to=total - sp)
], "v", total, audio_delay=3.0)

# scene 06
total = A("06") + LEAD
sp = (93.0 - 3.0) / 8
run("06", [T("06")], [
    seg(0, 3.0, 93.0, 8, labels=[label(SPED, f"between(t,0,{sp:.2f})"), label(SAME, f"gt(t,{sp:.2f})")], hold_to=total - sp)
], "v", total)

# scene 08: SOURCES.md (real time) then the override run (sped up, then held)
total = A("08") + LEAD
a_len = 17.4
sp = (81.0 - 3.0) / 8
run("08", [RAW9B, T("08")], [
    seg(0, 43.9, 43.9 + a_len, 1, mask=True, tag="va"),
    seg(1, 3.0, 81.0, 8, labels=[label(SPED, f"between(t,0,{sp:.2f})"), label(SAME, f"gt(t,{sp:.2f})")], hold_to=total - a_len - sp, tag="vb"),
    "[va][vb]concat=n=2:v=1:a=0[v]"
], "v", total)

# scene 09: selftest (real time) then core.py snapshot fallback
total = A("09") + LEAD
b_start = 5.5
run("09", [T("09"), RAW9B], [
    seg(0, 3.0, 3.0 + b_start, 1, tag="va"),
    seg(1, 11.03, 11.03 + (total - b_start), 1, mask=True, tag="vb"),
    "[va][vb]concat=n=2:v=1:a=0[v]"
], "v", total)


# scene 07: architecture image, front, price, logistics profiles, architecture again; boundaries from sentence lengths
# price/logistics shots come from raw07b (retake after the helper profiles were branded); the rest from raw07
RAW7 = os.path.join(CLIPS, "raw07.mp4")
RAW7B = os.path.join(CLIPS, "raw07b.mp4")
total = A("07") + LEAD
b = [0, 5.4, 17.2, 21.6, 27.6, total]  # section boundaries in scene time
arch0, front0 = 88.96, 1.16
price0, logi0 = 30.50, 1.20  # offsets inside raw07b
run("07", [RAW7, RAW7B], [
    seg(0, arch0, arch0 + (b[1] - b[0]), 1, mask=True, tag="v0"),
    seg(0, front0, front0 + (b[2] - b[1]), 1, mask=True, tag="v1"),
    seg(1, price0, price0 + (b[3] - b[2]), 1, mask=True, tag="v2"),
    seg(1, logi0, logi0 + (b[4] - b[3]), 1, mask=True, tag="v3"),
    seg(0, arch0 + (b[1] - b[0]), arch0 + (b[1] - b[0]) + (b[5] - b[4]), 1, mask=True, tag="v4"),
    "[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[v]"
], "v", total)


# scene 04 re-timed in post: card changes follow the sentences (boundaries from sentence lengths: 17.3, 22.7, 34.4 s)
RAW4 = os.path.join(CLIPS, "raw04.mp4")
o = 2.04
total = A("04") + LEAD
t1 = 16.6          # start of scroll to row 2
t2 = 22.0          # start of scroll to row 3
t3 = 33.6          # start of scroll back to row 1
hold1_raw = 12.5
run("04", [RAW4], [
    seg(0, o, o + hold1_raw, 1, mask=True, hold_to=t1 - hold1_raw, tag="p0"),
    seg(0, o + 12.5, o + 14.0, 1, mask=True, tag="p1"),
    seg(0, o + 14.0, o + 14.0 + (t2 - t1 - 1.5), 1, mask=True, tag="p2"),
    seg(0, o + 18.0, o + 19.5, 1, mask=True, tag="p3"),
    seg(0, o + 19.5, o + 19.5 + (t3 - t2 - 1.5), 1, mask=True, tag="p4"),
    seg(0, o + 32.0, o + 34.5, 1, mask=True, tag="p5"),
    seg(0, o + 34.5, o + 34.5 + (total - t3 - 2.5), 1, mask=True, tag="p6"),
    "[p0][p1][p2][p3][p4][p5][p6]concat=n=7:v=1:a=0[v]"
], "v", total)

# scene 01 re-timed in post: the answer image arrives while "same price ... 2,500" is spoken
RAW1 = os.path.join(CLIPS, "raw01.mp4")
o = 1.15
total = A("01") + LEAD
run("01", [RAW1], [
    seg(0, o, o + 3.0, 1, mask=True, tag="q0"),
    seg(0, o + 8.5, o + 13.5, 1, mask=True, tag="q1"),
    seg(0, o + 13.5, o + 22.0, 1, mask=True, hold_to=max(0.0, total - 8.0 - 8.5), tag="q2"),
    "[q0][q1][q2]concat=n=3:v=1:a=0[v]"
], "v", total)
