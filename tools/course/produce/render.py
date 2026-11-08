"""Render a lesson video from its narration timeline and its visuals.py.

    <kokoro-venv>/bin/python -I tools/course/produce/render.py course/modules/M00/M00.01

Needs render/timeline.json, render/narration.wav and render/captions.vtt (narrate.py, then
normalize_and_check.sh). The lesson's visuals.py defines

    frame(scene: int, index: int) -> PIL.Image   # the picture while sentence `index` of `scene` is spoken

Each picture appears LEAD seconds before its sentence starts and stays until the next one.
Identical consecutive pictures are merged, so a static slide is one still in the video.

Writes render/<lesson>.mp4 (H.264 + AAC + soft mov_text English subtitles, 1920x1080, 30 fps),
render/frames/*.png, and render/contact_sheet.png (every distinct picture, for review).
"""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
LEAD = 0.25


def load_visuals(lesson_dir):
    spec = importlib.util.spec_from_file_location(
        "visuals", Path(lesson_dir) / "visuals.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def contact_sheet(pngs, out, cols=5, tw=384):
    th = tw * 9 // 16
    rows = -(-len(pngs) // cols)
    sheet = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 8) + 8), "#000000")
    for i, p in enumerate(pngs):
        im = Image.open(p).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
    sheet.save(out)


def main(lesson_dir):
    d = Path(lesson_dir) / "render"
    tl = json.loads((d / "timeline.json").read_text())
    visuals = load_visuals(lesson_dir)
    frames = d / "frames"
    frames.mkdir(exist_ok=True)
    for old in frames.glob("*.png"):
        old.unlink()

    shots = []  # [start_time, png_path, digest]
    for k, s in enumerate(tl["sentences"]):
        im = visuals.frame(s["scene"], s["index"])
        assert im.size == (1920, 1080), f"scene {s['scene']} #{s['index']}: {im.size}"
        digest = hashlib.sha1(im.tobytes()).hexdigest()
        if shots and shots[-1][2] == digest:
            continue
        png = frames / f"{len(shots):03d}_s{s['scene']:02d}_{s['index']:02d}.png"
        im.save(png)
        start = 0.0 if k == 0 else max(s["start"] - LEAD, shots[-1][0] + 0.1)
        shots.append([start, png, digest])

    lines = []
    for i, (start, png, _) in enumerate(shots):
        end = shots[i + 1][0] if i + 1 < len(shots) else tl["duration"]
        lines += [f"file '{png.resolve()}'", f"duration {end - start:.3f}"]
    lines.append(
        f"file '{shots[-1][1].resolve()}'"
    )  # the concat demuxer needs the last file repeated
    concat = d / "frames.txt"
    concat.write_text("\n".join(lines) + "\n")

    out = d / f"{tl['lesson']}.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-i",
            str(d / "narration.wav"),
            "-i",
            str(d / "captions.vtt"),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-map",
            "2:s",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-tune",
            "stillimage",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            "fps=30",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-c:s",
            "mov_text",
            "-metadata:s:s:0",
            "language=eng",
            "-metadata",
            f"title={tl['lesson']} — {tl['title']}",
            "-movflags",
            "+faststart",
            "-t",
            f"{tl['duration']:.3f}",
            str(out),
        ],
        check=True,
    )
    contact_sheet([p for _, p, _ in shots], d / "contact_sheet.png")
    print(f"{out}  ({len(shots)} distinct frames, {tl['duration']:.1f}s)")


if __name__ == "__main__":
    main(sys.argv[1])
