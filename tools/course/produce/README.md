# Lesson production pipeline

Turns a lesson package (`script.md` + `visuals.py`) into a narrated 1920×1080 MP4 with soft English subtitles.
Free, local tools only: Kokoro 0.9.4 (voice `af_heart`), ffmpeg, faster-whisper, Pillow. The virtualenvs live outside the repo, in `../tools/kokoro/.venv` and `../tools/whisper/.venv`.

Run from the repository root, for example with `L=course/modules/M00/M00.01`:

| Step | Command | Writes (in `$L/render/`, git-ignored) |
|---|---|---|
| 1. Narrate | `../tools/kokoro/.venv/bin/python -I tools/course/produce/narrate.py $L` | `narration_raw.wav`, `timeline.json`, `captions.vtt` |
| 2. Normalize and check | `bash tools/course/produce/normalize_and_check.sh $L` | `narration.wav` (-16 LUFS, -1.5 dBTP, 48 kHz), `checks.txt` |
| 3. Speech check | `../tools/whisper/.venv/bin/python -I tools/course/produce/asr_check.py $L` | `asr.txt` (word error rate and diffs against the spoken text) |
| 4. Render | `../tools/kokoro/.venv/bin/python -I tools/course/produce/render.py $L` | `<lesson>.mp4`, `frames/`, `contact_sheet.png` |

- `script_parser.py`: the one parser for `script.md`. A sentence's caption is the line as written; an optional `> spoken:` line below it is what Kokoro says (see `course/style/PRONUNCIATION.md`).
- `slides.py`: palette, fonts and drawing helpers shared by every lesson's `visuals.py`. Keep the bottom 150 px clear for subtitles.
- `visuals.py` (per lesson): `frame(scene, index)` returns the picture shown while that sentence is spoken. Terminal text in it must be real, captured output, with its source noted at the top of the file.

The speech check isn't a listening review. When it flags a word, transcribe that sentence on its own before changing the script. Whisper's long-form decoding makes context errors: in M0.1, "Simulated" was heard as "it's not related" in the full track, but correctly by both `base.en` and `small.en` on the sentence alone.
