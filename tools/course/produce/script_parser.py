"""Parse a lesson script.md into scenes of (caption, spoken) sentences.

Shared by the narration, render and check steps, so the script is the single
source of truth for what is said and what is shown as captions.
"""

import re
from pathlib import Path


def parse(script_path):
    """Return {"id": "M00.01", "title": str, "scenes": [{"no", "name", "sentences": [(caption, spoken)]}]}."""
    text = Path(script_path).read_text()
    head = re.search(r"^# (M\d\d\.\d\d) — (.+)$", text, re.MULTILINE)
    lines = text.splitlines()
    scenes, scene, in_comment = [], None, False
    for i, raw in enumerate(lines):
        s = raw.strip()
        if s.startswith("<!--"):
            in_comment = "-->" not in s
            continue
        if in_comment:
            in_comment = "-->" not in s
            continue
        m = re.match(r"### Scene (\d+) — (.+)", s)
        if m:
            scene = {"no": int(m.group(1)), "name": m.group(2).strip(), "sentences": []}
            scenes.append(scene)
            continue
        if scene is None or not s or s == "---" or s.startswith(("#", "> spoken:")):
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        spoken = (
            nxt.removeprefix("> spoken:").strip() if nxt.startswith("> spoken:") else s
        )
        scene["sentences"].append((s, spoken))
    return {"id": head.group(1), "title": head.group(2).strip(), "scenes": scenes}
