"""Drawing helpers shared by every lesson's visuals.py (1920x1080, the pilot's palette).

Rules carried over from the pilot review:
- Keep y > SAFE_BOTTOM clear: players draw subtitles there.
- Helvetica.ttc has no glyph for "✓", "✗" or "→" (they render as an empty box), so ticks
  and arrows are drawn as shapes (tick(), arrow()), and inline arrows use "›".
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
MARGIN = 96
SAFE_BOTTOM = H - 150
BG, PANEL, TEXT, MUTED = "#0f172a", "#1e293b", "#e2e8f0", "#64748b"
AMBER, TEAL, DIM, RED = "#fbbf24", "#2dd4bf", "#334155", "#f87171"
HILITE = "#3f3a1d"  # amber-tinted background behind highlighted code
MONO = "/System/Library/Fonts/Menlo.ttc"
SANS = "/System/Library/Fonts/Helvetica.ttc"

# Honesty-label badges (STYLE_GUIDE.md, "Honesty labels"): background, text colour.
BADGES = {
    "Simulated": ("#78350f", "#fde68a"),
    "Prepared-only": ("#1e3a8a", "#bfdbfe"),
    "Hypothesis": ("#4c1d95", "#ddd6fe"),
}

_cache = {}


def font(size, bold=False, mono=False):
    key = (size, bold, mono)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(
            MONO if mono else SANS, size, index=1 if bold else 0
        )
    return _cache[key]


def canvas(header):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((MARGIN, 56), header, font=font(28), fill=MUTED)
    return im, d


def wrap(text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and f.getlength(trial) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur] if cur else lines


def paragraph(d, xy, text, f, fill, width, leading=1.3):
    """Draw wrapped text; return the y below the last line."""
    x, y = xy
    for line in wrap(text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += int(f.size * leading)
    return y


def centered(d, y, text, f, fill):
    d.text(((W - f.getlength(text)) / 2, y), text, font=f, fill=fill)


def title(d, text, y=130, size=60):
    d.text((MARGIN, y), text, font=font(size, bold=True), fill=TEXT)


def takeaway(d, text, y=820):
    centered(d, y, text, font(38), TEXT)


def card(d, box, heading, body="", on=True, accent=TEAL, hsize=38, bsize=30):
    x0, y0, x1, _ = box
    d.rounded_rectangle(
        box, radius=22, fill=PANEL, outline=accent if on else DIM, width=5 if on else 2
    )
    y = paragraph(
        d,
        (x0 + 32, y0 + 30),
        heading,
        font(hsize, bold=True),
        TEXT if on else MUTED,
        x1 - x0 - 64,
    )
    if body:
        paragraph(
            d, (x0 + 32, y + 14), body, font(bsize), TEXT if on else MUTED, x1 - x0 - 64
        )


def badge(d, xy, label, size=34):
    bg, fg = BADGES[label]
    f = font(size, bold=True)
    x, y = xy
    w = f.getlength(label)
    d.rounded_rectangle(
        (x, y, x + w + 2 * size * 0.7, y + size * 1.8), radius=int(size * 0.5), fill=bg
    )
    d.text((x + size * 0.7, y + size * 0.38), label, font=f, fill=fg)
    return x + w + 2 * size * 0.7


def tick(d, xy, size=34, fill=TEAL):
    x, y = xy
    d.line(
        [
            (x, y + size * 0.55),
            (x + size * 0.38, y + size * 0.9),
            (x + size, y + size * 0.1),
        ],
        fill=fill,
        width=max(4, size // 7),
        joint="curve",
    )


def cross(d, xy, size=34, fill=RED):
    x, y = xy
    w = max(4, size // 7)
    d.line([(x, y), (x + size, y + size)], fill=fill, width=w)
    d.line([(x + size, y), (x, y + size)], fill=fill, width=w)


def arrow(d, a, b, fill=TEAL, width=6, head=22):
    (x0, y0), (x1, y1) = a, b
    d.line((x0, y0, x1, y1), fill=fill, width=width)
    import math

    ang = math.atan2(y1 - y0, x1 - x0)
    pts = [(x1, y1)]
    for s in (-1, 1):
        pts.append(
            (
                x1 - head * math.cos(ang) + s * head * 0.6 * math.sin(ang),
                y1 - head * math.sin(ang) - s * head * 0.6 * math.cos(ang),
            )
        )
    d.polygon(pts, fill=fill)


def terminal(d, box, lines, size=26, label="Terminal"):
    """Draw a terminal window. lines: list of str or list of [(text, colour, highlighted)] runs."""
    x0, y0, x1, _ = box
    d.rounded_rectangle(box, radius=16, fill="#0b1120", outline=DIM, width=2)
    d.rounded_rectangle((x0, y0, x1, y0 + 48), radius=16, fill=PANEL)
    d.rectangle((x0, y0 + 30, x1, y0 + 48), fill=PANEL)
    for i, c in enumerate(("#ef4444", "#f59e0b", "#22c55e")):
        d.ellipse((x0 + 22 + i * 30, y0 + 16, x0 + 38 + i * 30, y0 + 32), fill=c)
    lf = font(22)
    d.text(((x0 + x1 - lf.getlength(label)) / 2, y0 + 12), label, font=lf, fill=MUTED)
    f = font(size, mono=True)
    lh = int(size * 1.32)
    y = y0 + 70
    maxw = x1 - x0 - 64
    for line in lines:
        runs = [(line, TEXT, False)] if isinstance(line, str) else line
        x = x0 + 32
        for text, col, hi in runs:
            text = text.replace("\t", "    ")  # Menlo draws a tab as an empty box
            if (
                x - x0 - 32 + f.getlength(text) > maxw
            ):  # clip, never overflow the window
                while text and x - x0 - 32 + f.getlength(text + "…") > maxw:
                    text = text[:-1]
                text += "…"
            w = f.getlength(text)
            if hi:
                d.rounded_rectangle(
                    (x - 6, y - 4, x + w + 6, y + lh - 4), radius=6, fill=HILITE
                )
            d.text((x, y), text, font=f, fill=col)
            x += w
        y += lh
    return y
