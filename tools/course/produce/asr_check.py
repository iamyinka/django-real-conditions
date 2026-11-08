"""Transcribe the narration with a local Whisper model and compare it with the script.

    <whisper-venv>/bin/python -I tools/course/produce/asr_check.py course/modules/M00/M00.01

Catches dropped, repeated or garbled words. It is NOT a listening review: it can't judge
tone or naturalness, and Whisper makes its own mistakes. Writes render/asr.txt.
"""

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

NUMBERS = {
    "zero": "0",
    "oh": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
}


COMPOUNDS = {
    "tool chain": "toolchain",
    "pre commit": "precommit",
    "pie test": "pytest",
    "intra net": "intranet",
    # Spelling variants of the same spoken words (script form on the right).
    "mac os": "macos",
    "file system": "filesystem",
    "okay": "ok",
    "a p i": "api",
    "no reply": "noreply",
    "soo doo": "sudo",
}
WORDNUM = {
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "twenty": "20",
    "thirty": "30",
    "forty": "40",
    "fifty": "50",
    "hundred": "100",
}


def words(text):
    # Whisper writes spoken "dash dash version" as "--version".
    t = text.lower().replace("--", " dash dash ").replace("-", " ")
    t = re.sub(r"\bpostgres(ql)?\b", "postgres", t)
    t = re.sub(r"\b(\d+) ?gb\b", r"\1 gigabytes", t)
    for a, b in COMPOUNDS.items():
        t = t.replace(a, b)
    toks = [NUMBERS.get(w, WORDNUM.get(w, w)) for w in re.findall(r"[a-z0-9']+", t)]
    out, run = (
        [],
        False,
    )  # merge runs of single letters ("v p n" -> "vpn") and digits ("5 4 3 2")
    for w in toks:
        single = len(w) == 1 and w not in ("a", "i")
        if single and run:
            out[-1] += w
        else:
            out.append(w)
        run = single
    return out


def main(lesson_dir):
    d = Path(lesson_dir) / "render"
    tl = json.loads((d / "timeline.json").read_text())
    ref = words(" ".join(s["spoken"] for s in tl["sentences"]))
    pcm = subprocess.run(
        [
            "ffmpeg",
            "-loglevel",
            "error",
            "-i",
            str(d / "narration.wav"),
            "-f",
            "f32le",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-",
        ],
        capture_output=True,
        check=True,
    ).stdout
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(
        np.frombuffer(pcm, np.float32), language="en", beam_size=5
    )
    hyp_text = " ".join(s.text.strip() for s in segs)
    hyp = words(hyp_text)
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    errs, report = 0, []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            errs += max(i2 - i1, j2 - j1)
            report.append(
                f"{op:8} script: {' '.join(ref[i1:i2])!r:45} heard: {' '.join(hyp[j1:j2])!r}"
            )
    wer = errs / len(ref)
    (d / "asr.txt").write_text(
        f"WER {wer:.1%} ({errs}/{len(ref)})\n\nTRANSCRIPT:\n{hyp_text}\n\n"
        "DIFFS:\n" + "\n".join(report) + "\n"
    )
    print(f"{tl['lesson']}: WER {wer:.1%} ({errs}/{len(ref)} words)")
    for line in report:
        print("   ", line)
    # Context for each diff, so a human can judge whether it's the voice or Whisper.
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            print(f"  [{op}] script: ...{' '.join(ref[max(i1 - 6, 0) : i2 + 6])}...")
            print(f"           heard: ...{' '.join(hyp[max(j1 - 6, 0) : j2 + 6])}...")


if __name__ == "__main__":
    main(sys.argv[1])
