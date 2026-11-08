"""Synthesize a lesson's narration with Kokoro, using the settings approved in the pilot.

    <kokoro-venv>/bin/python -I tools/course/produce/narrate.py course/modules/M00/M00.01

Writes into <lesson>/render/:
    narration_raw.wav   24 kHz mono, before loudness normalization
    timeline.json       per-sentence timing, used by render.py and asr_check.py
    captions.vtt        WebVTT cues from the caption text, timed by the synthesized audio

Approved settings (pilot/README.md, "Decision"): voice af_heart, sentence-by-sentence
synthesis, speed 0.95, 0.4 s between sentences, 0.9 s between scenes, Kokoro's own edge
silence trimmed so those gaps are exact.
"""

import json
import re
import sys
import textwrap
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).parent))
from script_parser import parse

SR = 24_000
VOICE, LANG, SPEED = "af_heart", "a", 0.95
LEAD_IN, TAIL = 0.5, 1.5
SENTENCE_GAP, SCENE_GAP = 0.40, 0.90
EDGE_PAD = 0.06


def silence(seconds):
    return np.zeros(int(SR * seconds), dtype=np.float32)


def synth(pipeline, text):
    chunks = [
        r.audio.numpy()
        for r in pipeline(text, voice=VOICE, speed=SPEED, split_pattern=None)
    ]
    audio = np.concatenate(chunks).astype(np.float32)
    loud = np.flatnonzero(np.abs(audio) > 0.01)
    pad = int(SR * EDGE_PAD)
    return audio[max(loud[0] - pad, 0) : min(loud[-1] + pad, len(audio))]


def fmt(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def caption_cues(text, start, end, max_chars=84):
    """Split long sentences into balanced cues at word boundaries, preferring punctuation.
    Each cue is timed by its share of characters (Kokoro gives sentence-level timing only)."""
    n = -(-len(text) // max_chars)
    words = text.split()
    ends, pos = [], 0
    for w in words:
        pos += len(w) + (1 if ends else 0)
        ends.append(pos)
    breaks = []
    for k in range(1, n):
        ideal = len(text) * k / n

        def cost(i, ideal=ideal):
            bonus = (
                25
                if re.search(r"[.?!]$", words[i])
                else 12
                if re.search(r"[,:;]$", words[i])
                else 0
            )
            return abs(ends[i] - ideal) - bonus

        candidates = [i for i in range(len(words) - 1) if not breaks or i > breaks[-1]]
        breaks.append(min(candidates, key=cost))
    parts, prev = [], 0
    for b in breaks + [len(words) - 1]:
        parts.append(" ".join(words[prev : b + 1]))
        prev = b + 1
    total = sum(len(p) for p in parts)
    cues, t = [], start
    for p in parts:
        dur = (end - start) * len(p) / total
        cues.append((t, t + dur, "\n".join(textwrap.wrap(p, 42))))
        t += dur
    return cues


def main(lesson_dir):
    from kokoro import KPipeline

    lesson = parse(Path(lesson_dir) / "script.md")
    out = Path(lesson_dir) / "render"
    out.mkdir(exist_ok=True)
    pipeline = KPipeline(lang_code=LANG, repo_id="hexgrad/Kokoro-82M")

    audio, sentences, scenes, cues, t = [silence(LEAD_IN)], [], [], [], LEAD_IN
    for si, scene in enumerate(lesson["scenes"]):
        if si:
            audio.append(silence(SCENE_GAP))
            t += SCENE_GAP
        scenes.append({"no": scene["no"], "name": scene["name"], "start": round(t, 3)})
        for i, (caption, spoken) in enumerate(scene["sentences"]):
            if i:
                audio.append(silence(SENTENCE_GAP))
                t += SENTENCE_GAP
            clip = synth(pipeline, spoken)
            audio.append(clip)
            start, end = t, t + len(clip) / SR
            sentences.append(
                {
                    "scene": scene["no"],
                    "index": i,
                    "start": round(start, 3),
                    "end": round(end, 3),
                    "caption": caption,
                    "spoken": spoken,
                }
            )
            cues += caption_cues(caption.replace("`", ""), start, end)
            t = end
        print(f"  scene {scene['no']:2} {scene['name']:<34} ends {t:6.1f}s", flush=True)
    audio.append(silence(TAIL))
    t += TAIL

    sf.write(out / "narration_raw.wav", np.concatenate(audio), SR, subtype="PCM_16")
    (out / "timeline.json").write_text(
        json.dumps(
            {
                "lesson": lesson["id"],
                "title": lesson["title"],
                "voice": VOICE,
                "speed": SPEED,
                "duration": round(t, 3),
                "scenes": scenes,
                "sentences": sentences,
            },
            indent=2,
        )
    )
    vtt = ["WEBVTT", ""]
    for n, (a, b, txt) in enumerate(cues, 1):
        vtt += [str(n), f"{fmt(a)} --> {fmt(b)}", txt, ""]
    (out / "captions.vtt").write_text("\n".join(vtt))
    print(
        f"{lesson['id']}: {t:.1f}s narration, {len(sentences)} sentences, {len(cues)} caption cues"
    )


if __name__ == "__main__":
    main(sys.argv[1])
