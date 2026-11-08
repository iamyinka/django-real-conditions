"""Mechanical checks for lesson scripts and storyboards.

    python3 tools/course/check_lesson.py course/modules/M01/M01.05 [more lesson dirs...]

Checks (errors fail the run, warnings don't):
- script.md, storyboard.md, notes.md, exercise.md all exist
- script scenes and storyboard scenes have the same numbers
- the spoken text contains no raw code (backticks, paths, flags, underscores, file
  extensions) and no caption forms the pronunciation glossary replaces
- estimated narration time vs. the target and vs. each storyboard scene's duration

Narration time uses the approved pilot's measured rate: 172 words in 72.2 s, including
the pipeline's sentence and scene gaps, which is about 143 words per minute.
This is a planning estimate. The rendered audio is the real measurement.
"""

import re
import sys
from pathlib import Path

WPM = 172 / 72.2 * 60  # ≈ 143

# (pattern, why). Applied to spoken text only.
SPOKEN_BANNED = [
    (r"`", "backtick: describe code instead of reading it"),
    (r"(?<!\w)--\w", "flag with dashes: say 'the dash-dash check flag'"),
    (r"\w_\w", "underscore: say the words, e.g. 'wait for D B'"),
    (r"\w/\w", "slash path: describe the place instead"),
    (
        r"\.(py|yaml|yml|toml|lock|md|txt|sh)\b",
        "file extension: use the 'dot py' spoken form",
    ),
    (r"\bPostgreSQL\b", "glossary: say 'Postgres'"),
    (r"\bYAML\b", "glossary: lowercase 'yaml', or it's spelled out"),
    (r"\bdb\b", "glossary: the service name is spoken 'D B'"),
    (r"[{}<>=$|]", "code symbol in spoken text"),
]


def spoken_lines(script):
    """Yield (scene_no, line_no, spoken_text) for every narrated sentence."""
    lines = script.splitlines()
    scene = None
    in_comment = False
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("<!--"):
            in_comment = "-->" not in s
            continue
        if in_comment:
            in_comment = "-->" not in s
            continue
        m = re.match(r"### Scene (\d+)", s)
        if m:
            scene = int(m.group(1))
            continue
        if scene is None or not s or s == "---" or s.startswith(("#", "> spoken:")):
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        text = (
            nxt.removeprefix("> spoken:").strip() if nxt.startswith("> spoken:") else s
        )
        yield scene, i + 1, text


def check(lesson_dir):
    d = Path(lesson_dir)
    errors, warnings = [], []
    for name in ("script.md", "storyboard.md", "notes.md", "exercise.md"):
        if not (d / name).exists():
            errors.append(f"missing {name}")
    if errors:
        return errors, warnings, {}

    script = (d / "script.md").read_text()
    board = (d / "storyboard.md").read_text()
    target = int(re.search(r"\*\*Target length:\*\* (\d+) min", script).group(1))

    words_by_scene = {}
    for scene, ln, text in spoken_lines(script):
        words_by_scene[scene] = words_by_scene.get(scene, 0) + len(text.split())
        for pat, why in SPOKEN_BANNED:
            if re.search(pat, text):
                errors.append(f"script.md:{ln}: {why}: {text[:70]!r}")

    board_scenes = {
        int(m.group(1)): int(m.group(2))
        for m in re.finditer(r"^\| (\d+) \|.*\| (\d+) \|$", board, re.MULTILINE)
    }
    if set(words_by_scene) != set(board_scenes):
        errors.append(
            f"scene mismatch: script {sorted(words_by_scene)} vs storyboard {sorted(board_scenes)}"
        )

    for scene, words in words_by_scene.items():
        need = words / WPM * 60
        have = board_scenes.get(scene, 0)
        if have and need > have * 1.1:
            warnings.append(
                f"scene {scene}: narration ≈{need:.0f}s but storyboard allows {have}s"
            )

    words = sum(words_by_scene.values())
    narration_min = words / WPM
    board_min = sum(board_scenes.values()) / 60
    if not 0.8 * target <= board_min <= 1.2 * target:
        warnings.append(f"storyboard total {board_min:.1f} min vs target {target} min")
    stats = {
        "target": target,
        "words": words,
        "narration_min": round(narration_min, 1),
        "storyboard_min": round(board_min, 1),
    }
    return errors, warnings, stats


def main(argv):
    failed = False
    for lesson in argv:
        errors, warnings, stats = check(lesson)
        print(f"{lesson}: {stats}")
        for e in errors:
            print(f"  ERROR {e}")
        for w in warnings:
            print(f"  warn  {w}")
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
