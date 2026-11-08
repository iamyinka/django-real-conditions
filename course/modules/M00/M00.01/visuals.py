"""M00.01 visuals: one picture per narrated sentence (see storyboard.md).

Terminal text is real output, captured 2026-11-08 in this repository:
  scene 6: `git tag -l 'lesson/M01.0*'` and `git diff --stat lesson/M01.05-start lesson/M01.05-end`
  scene 7: the M1.5 error, as recorded in course/modules/M01/M01.05/notes.md
  scene 8: excerpts of course/modules/M01/M01.05/notes.md
"""

from slides import (
    AMBER,
    DIM,
    MARGIN,
    MUTED,
    PANEL,
    RED,
    TEAL,
    TEXT,
    W,
    arrow,
    badge,
    canvas,
    card,
    centered,
    cross,
    font,
    paragraph,
    takeaway,
    terminal,
    tick,
    title,
)

HEADER = "M0.1  ·  How this course works"


# Scene 1 — The gap
INCIDENTS = [
    (
        "Saved three times, offline",
        "A technician in a basement taps “save” with no signal.",
    ),
    ("Same technician, same second", "Two dispatchers assign one person at once."),
    ("Deploy without migrate", "The code is new. The database isn't."),
]


def scene1(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "“It works on my laptop.”", y=380, size=84)
        return im
    title(d, "Real work starts after the page loads.")
    shown = min(max(i - 1, 0), 3)
    cw = (W - 2 * MARGIN - 2 * 40) // 3
    for k in range(shown):
        x0 = MARGIN + k * (cw + 40)
        card(
            d,
            (x0, 300, x0 + cw, 640),
            *INCIDENTS[k],
            on=(k == i - 2 or i == 5),
            accent=AMBER,
        )
    if i == 5:
        takeaway(d, "This course: Django when the conditions aren't friendly.", y=720)
    return im


# Scene 2 — Five projects
PROJECTS = [
    ("telecom", "Field service. Technicians work offline and sync later."),
    ("telehealth", "Appointments, private documents, video calls."),
    ("streaming", "Learners on slow, expensive connections."),
    ("labtrack", "Specimens and live courier locations."),
    ("intranet", "Reachable only on the office network or a VPN."),
]


def scene2(i):
    im, d = canvas(HEADER)
    title(d, "Five projects, five kinds of business")
    gap = 24
    cw = (W - 2 * MARGIN - 4 * gap) // 5
    for k, (name, line) in enumerate(PROJECTS):
        x0 = MARGIN + k * (cw + gap)
        on = i == 0 or i == 6 or k == i - 1 or (i == 7 and k == 0)
        top, bottom = (280, 700) if (i == 7 and k == 0) else (320, 660)
        card(
            d,
            (x0, top, x0 + cw, bottom),
            f"{k + 1}  {name}",
            line,
            on=on,
            hsize=34,
            bsize=28,
        )
    if i == 6:
        for k in range(4):
            x = MARGIN + (k + 1) * (cw + gap) - gap
            arrow(
                d,
                (x - cw // 2 + 40, 700),
                (x + cw // 2 - 20, 700),
                fill=TEAL,
                width=4,
                head=16,
            )
        takeaway(d, "Each project reuses what the earlier ones taught.", y=750)
    if i == 7:
        takeaway(d, "Project 1 gets the most time: the foundations go in there.", y=750)
    return im


# Scene 3 — What "real conditions" means
POINTS = [
    "Containers, Git, pull requests: the way teams run code",
    "Break it on purpose, read the error, fix it",
    "Every claim checked: you see the command do it",
]


def scene3(i):
    im, d = canvas(HEADER)
    title(d, "“Real conditions” means three things")
    for k in range(min(i, 3)):
        y = 330 + k * 150
        on = k == i - 1
        d.ellipse((MARGIN, y, MARGIN + 84, y + 84), fill=AMBER if on else DIM)
        n = str(k + 1)
        f = font(46, bold=True)
        d.text(
            (MARGIN + 42 - f.getlength(n) / 2, y + 16),
            n,
            font=f,
            fill="#0f172a" if on else TEXT,
        )
        d.text(
            (MARGIN + 130, y + 18), POINTS[k], font=font(44), fill=TEXT if on else MUTED
        )
    return im


# Scene 4 — WHAT, WHERE, WHY (the pilot's three-places diagram)
TOKENS = ["docker compose", "exec", "web", "python manage.py migrate"]
BOXES = [
    ("Your machine (host)", ["terminal", "project folder", "compose.yaml"]),
    ("web container", ["Django", "manage.py", "your code"]),
    ("db container", ["Postgres", "tables", "migration records"]),
]
QUESTIONS = [("WHAT", "does it do?"), ("WHERE", "does it run?"), ("WHY", "this way?")]


def questions(d, active, y=330):
    cw = (W - 2 * MARGIN - 2 * 40) // 3
    for k, (q, rest) in enumerate(QUESTIONS):
        if k >= active[0]:
            continue
        x0 = MARGIN + k * (cw + 40)
        on = k in active[1]
        d.rounded_rectangle(
            (x0, y, x0 + cw, y + 220),
            radius=22,
            fill=PANEL,
            outline=AMBER if on else DIM,
            width=5 if on else 2,
        )
        d.text(
            (x0 + 40, y + 40), q, font=font(72, bold=True), fill=AMBER if on else TEXT
        )
        d.text((x0 + 40, y + 140), rest, font=font(40), fill=TEXT if on else MUTED)


def scene4(i):
    im, d = canvas(HEADER)
    if i <= 4 or i == 11:
        title(d, "Three answers for every command")
        shown, hot = {
            0: (0, ()),
            1: (1, (0,)),
            2: (2, (1,)),
            3: (3, (2,)),
            4: (3, (1,)),
            11: (3, (0, 1, 2)),
        }[i]
        questions(d, (shown, hot))
        if i == 4:
            takeaway(d, "WHERE is the one most tutorials skip.", y=640)
        if i == 11:
            takeaway(d, "Lost? Ask WHAT, WHERE and WHY.", y=640)
        return im
    # i 5..10: the command, then the three places.
    hi = {5: set(), 6: {0, 1, 2, 3}, 7: {0}, 8: {1, 2, 3}, 9: {3}, 10: {0, 1, 2, 3}}[i]
    boxes_on = {5: set(), 6: set(), 7: {0}, 8: {0, 1}, 9: {1, 2}, 10: {0, 1, 2}}[i]
    arrows_on = {8: {0}, 9: {1}, 10: {0, 1}}.get(i, set())
    mono = font(48, mono=True)
    d.rounded_rectangle((MARGIN, 140, W - MARGIN, 270), radius=18, fill=PANEL)
    x = 140
    d.text((x, 177), "$", font=mono, fill=MUTED)
    x += mono.getlength("$ ")
    for k, tok in enumerate(TOKENS):
        w = mono.getlength(tok)
        if k in hi and len(hi) < len(TOKENS):
            d.rounded_rectangle(
                (x - 10, 168, x + w + 10, 242), radius=10, fill="#3f3a1d"
            )
        d.text(
            (x, 177),
            tok,
            font=mono,
            fill=AMBER if k in hi else (TEXT if not hi or len(hi) == 4 else MUTED),
        )
        x += w + mono.getlength(" ")
    if i == 5:
        return im
    bw, bh, top = 440, 330, 380
    gap = (W - 2 * MARGIN - 3 * bw) // 2
    for k, (name, items) in enumerate(BOXES):
        x0 = MARGIN + k * (bw + gap)
        on = k in boxes_on
        d.rounded_rectangle(
            (x0, top, x0 + bw, top + bh),
            radius=22,
            fill=PANEL,
            outline=TEAL if on else DIM,
            width=5 if on else 2,
        )
        d.text(
            (x0 + 36, top + 34),
            name,
            font=font(38, bold=True),
            fill=TEXT if on else MUTED,
        )
        for j, it in enumerate(items):
            d.text(
                (x0 + 36, top + 110 + j * 56),
                "•  " + it,
                font=font(32),
                fill=TEXT if on else MUTED,
            )
    for k, label in enumerate((("compose", "exec"), ("Compose", "network"))):
        x0 = MARGIN + (k + 1) * bw + k * gap + 14
        x1 = x0 + gap - 28
        y = top + bh // 2
        col = TEAL if k in arrows_on else DIM
        arrow(d, (x0, y), (x1, y), fill=col)
        f = font(28)
        for j, part in enumerate(label):
            d.text(
                ((x0 + x1 - f.getlength(part)) / 2, y - 86 + j * 34),
                part,
                font=f,
                fill=TEXT if k in arrows_on else MUTED,
            )
    caption = {
        6: "One command. Where does each part run?",
        7: "WHERE: you type it in a terminal on your machine",
        8: "Docker runs the Python part inside the web container",
        9: "The tables it changes live in the db container",
        10: "Three places, one line.",
    }[i]
    takeaway(d, caption)
    return im


# Scene 5 — Honesty labels
LABELS = [
    (
        "Simulated",
        "A fake, built on purpose. Example: an SMS gateway that fails on command.",
    ),
    ("Prepared-only", "Configuration shown, not run in the recording."),
    ("Hypothesis", "A reasonable expectation we haven't measured yet."),
]


def scene5(i):
    im, d = canvas(HEADER)
    if i <= 2:
        title(d, "Some things can't be real on a laptop")
        for k, thing in enumerate(
            ["A real SMS provider", "Real patients", "A real GPS fleet"]
        ):
            if i == 0:
                break
            y = 320 + k * 110
            cross(d, (MARGIN + 10, y + 8), size=40)
            d.text((MARGIN + 90, y), thing, font=font(48), fill=TEXT)
        if i == 2:
            takeaway(d, "Stand-ins get a label on screen.", y=700)
        return im
    title(d, "Honesty labels")
    for k, (label, meaning) in enumerate(LABELS):
        if k > i - 3:
            break
        y = 290 + k * 140
        on = k == i - 3 or i == 6
        badge(d, (MARGIN, y), label, size=38)
        d.text(
            (MARGIN + 420, y + 14), meaning, font=font(38), fill=TEXT if on else MUTED
        )
    if i == 6:
        y = 290 + 3 * 140
        d.rounded_rectangle(
            (MARGIN, y, MARGIN + 330, y + 68), radius=19, outline=MUTED, width=2
        )
        d.text((MARGIN + 30, y + 14), "no label", font=font(38, bold=True), fill=MUTED)
        d.text(
            (MARGIN + 420, y + 14),
            "It ran. What you see is what happened.",
            font=font(38, bold=True),
            fill=TEAL,
        )
    return im


# Scene 6 — Checkpoints and exercises
TAGS = [
    f"lesson/M01.0{n}-{e}" for n in range(1, 10) for e in ("end", "start")
]  # git's sort order
DIFFSTAT = [
    " projects/telecom/.env.example            | 17 +++++++++++",
    " projects/telecom/compose.yaml            | 29 ++++++++++++++++++",
    " projects/telecom/config/settings/base.py | 13 +++++---",
    " projects/telecom/config/settings/test.py |  9 ++++++",
    " projects/telecom/pyproject.toml          |  1 +",
    " projects/telecom/uv.lock                 | 52 +++++++++++++++++++++++++++++++-",
    " 6 files changed, 116 insertions(+), 5 deletions(-)",
]


def tag_line(t, focus):
    col = TEAL if t.endswith("start") else AMBER
    return [
        (
            t,
            col if (focus is None or focus in t) else MUTED,
            focus is not None and t == focus,
        )
    ]


def scene6(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "One public Git repository")
        d.rounded_rectangle((MARGIN, 330, W - MARGIN, 470), radius=18, fill=PANEL)
        centered(
            d,
            368,
            "github.com/iamyinka/django-real-conditions",
            font(54, mono=True),
            TEXT,
        )
        takeaway(d, "Five projects, one repo, every lesson tagged.", y=560)
        return im
    if i in (1, 2):
        focus = None if i == 1 else "lesson/M01.05-start"
        lines = [[("$ ", MUTED, False), ("git tag -l 'lesson/M01.0*'", TEXT, False)]]
        lines += [tag_line(t, focus) for t in TAGS]
        terminal(d, (MARGIN, 110, 1100, 920), lines, size=24)
        x = 1160
        y = paragraph(
            d, (x, 220), "Two tags per lesson:", font(40, bold=True), TEXT, 660
        )
        d.text((x, y + 20), "-start", font=font(40, mono=True), fill=TEAL)
        d.text((x + 200, y + 24), "where it begins", font=font(36), fill=TEXT)
        d.text((x, y + 90), "-end", font=font(40, mono=True), fill=AMBER)
        d.text((x + 200, y + 94), "where it ends", font=font(36), fill=TEXT)
        if i == 2:
            paragraph(
                d,
                (x, y + 200),
                "Stuck? Check out the start tag and carry on.",
                font(38),
                AMBER,
                660,
            )
            d.rounded_rectangle(
                (x, y + 330, W - MARGIN, y + 400), radius=10, fill=PANEL
            )
            d.text(
                (x + 20, y + 346),
                "git switch --detach lesson/M01.05-start",
                font=font(24, mono=True),
                fill=TEXT,
            )
        return im
    if i == 3:
        lines = [
            [
                ("$ ", MUTED, False),
                ("git diff --stat lesson/M01.05-start lesson/M01.05-end", TEXT, False),
            ]
        ]
        lines += DIFFSTAT[:-1] + [[(DIFFSTAT[-1], AMBER, True)]]
        terminal(d, (MARGIN, 140, W - MARGIN, 560), lines, size=28)
        takeaway(
            d,
            "Compare your work with the end tag: the diff shows what you missed.",
            y=640,
        )
        return im
    # i 4..7: exercises
    title(d, "Most lessons end with an exercise")
    d.rounded_rectangle(
        (MARGIN, 260, 1180, 800),
        radius=22,
        fill=PANEL,
        outline=TEAL if i == 5 else DIM,
        width=5 if i == 5 else 2,
    )
    d.text(
        (MARGIN + 40, 290),
        "M1.5 exercise  ·  Acceptance criteria",
        font=font(34, bold=True),
        fill=TEXT,
    )
    crit = [
        "docker compose port db 5432  prints  127.0.0.1:5433",
        "A database client reaches the container's database",
        "Django still connects with DB_HOST=db, DB_PORT=5432",
        "You can explain why DB_PORT stays 5432",
    ]
    for k, c in enumerate(crit):
        y = 370 + k * 100
        d.rounded_rectangle(
            (MARGIN + 40, y, MARGIN + 84, y + 44), radius=8, outline=MUTED, width=3
        )
        if i == 5:
            tick(d, (MARGIN + 46, y + 4), size=34)
        paragraph(d, (MARGIN + 110, y + 4), c, font(30), TEXT if i >= 5 else MUTED, 960)
    if i >= 6:
        on = i == 6
        d.rounded_rectangle(
            (1240, 260, W - MARGIN, 800),
            radius=22,
            fill=PANEL,
            outline=AMBER if on else DIM,
            width=5 if on else 2,
        )
        d.text((1280, 290), "Solution", font=font(34, bold=True), fill=TEXT)
        paragraph(
            d,
            (1280, 370),
            "On its own tag, so you won't see it by accident:",
            font(30),
            TEXT,
            500,
        )
        d.text((1280, 480), "solution/M01.05", font=font(34, mono=True), fill=AMBER)
    if i == 7:
        takeaway(d, "Try the exercise before you look.", y=850)
    return im


# Scene 7 — Mistakes on purpose
ERR1 = (
    'psycopg.OperationalError: connection failed: connection to server at "127.0.0.1", '
)
ERR2 = "  port 5432 failed: Connection refused"
ERR3 = "  Is the server running on that host and accepting TCP/IP connections?"


def scene7(i):
    im, d = canvas(HEADER)
    if i <= 3:
        title(
            d, "A real error from Module 1" if i else "Failures are part of the lesson"
        )
        if i == 0:
            return im
        hot = i >= 2
        lines = [
            [
                ("$ ", MUTED, False),
                ("docker compose exec ", TEXT, False),
                ("-e DB_HOST=localhost", AMBER if i == 3 else TEXT, i == 3),
                (" web python manage.py migrate", TEXT, False),
            ],
            "...",
            [(ERR1, RED, False)],
            [
                ("  port ", RED, False),
                ("5432", RED, hot),
                (" failed: ", RED, False),
                ("Connection refused", RED, hot),
            ],
            [(ERR3, MUTED, False)],
        ]
        terminal(d, (MARGIN, 260, W - MARGIN, 640), lines, size=27)
        if i == 3:
            takeaway(d, "The settings say the database is at localhost.", y=700)
        return im
    # i 4..6: what localhost means inside a container
    title(d, "Inside a container, localhost is the container itself")
    bw, top, bh = 620, 330, 340
    wx, dx = MARGIN + 60, W - MARGIN - 60 - bw
    d.rounded_rectangle(
        (wx, top, wx + bw, top + bh), radius=22, fill=PANEL, outline=TEAL, width=5
    )
    d.text((wx + 36, top + 30), "web container", font=font(40, bold=True), fill=TEXT)
    d.text((wx + 36, top + 110), "Django: connect to", font=font(34), fill=TEXT)
    d.text((wx + 36, top + 160), "localhost:5432", font=font(36, mono=True), fill=AMBER)
    d.text((wx + 36, top + 230), "nothing listens here", font=font(34), fill=RED)
    d.arc(
        (wx + bw - 160, top - 70, wx + bw + 60, top + 130),
        start=200,
        end=110,
        fill=AMBER,
        width=6,
    )
    arrow(
        d,
        (wx + bw + 30, top + 108),
        (wx + bw - 10, top + 120),
        fill=AMBER,
        width=6,
        head=22,
    )
    d.rounded_rectangle(
        (dx, top, dx + bw, top + bh), radius=22, fill=PANEL, outline=DIM, width=2
    )
    d.text((dx + 36, top + 30), "db container", font=font(40, bold=True), fill=MUTED)
    d.text((dx + 36, top + 110), "Postgres listens on", font=font(34), fill=MUTED)
    d.text((dx + 36, top + 160), "db:5432", font=font(36, mono=True), fill=TEXT)
    for x in range(wx + bw + 40, dx - 30, 36):  # the connection that never happens
        d.line((x, top + bh // 2 + 40, x + 18, top + bh // 2 + 40), fill=DIM, width=5)
    text = {
        4: "No database in there: the connection is refused.",
        5: "Make it on purpose. Read it. Find the cause. Then fix it.",
        6: "Read the error before you search for it.",
    }[i]
    takeaway(d, text, y=760)
    return im


# Scene 8 — The notes behind each lesson
NOTES = [
    "### `docker compose up -d --build`",
    "- **Working directory:** `projects/telecom/`",
    "",
    "| Part | Meaning |",
    "|---|---|",
    "| `docker compose` | The Compose plugin; reads `compose.yaml` from the current directory |",
    "| `up` | Create the network, build or pull images, create and start containers |",
    "| `-d` | Detached: return the terminal; containers keep running |",
    "| `--build` | Rebuild images even if one exists |",
    "",
    "## Troubleshooting",
    "",
    "| Symptom | Fix |",
    "|---|---|",
    "| `Bind for 127.0.0.1:8001 failed: port is already allocated` | `docker ps` to find the owner; ...",
    "| `ImproperlyConfigured: Set the POSTGRES_DB…` | `cp .env.example .env` |",
    "| Changed `POSTGRES_PASSWORD` in `.env`, now `password authentication failed` | ...",
]
PARTS, TROUBLE = range(3, 9), range(10, 17)


def scene8(i):
    im, d = canvas(HEADER)
    hot = {2: PARTS, 3: TROUBLE}.get(i, range(0))
    lines = []
    for k, line in enumerate(NOTES):
        col = TEAL if line.startswith("#") else TEXT
        lines.append([(line, col if (not hot or k in hot) else MUTED, k in hot)])
    terminal(
        d,
        (MARGIN, 110, W - MARGIN, 760),
        lines,
        size=22,
        label="course/modules/M01/M01.05/notes.md",
    )
    text = {
        0: "The video covers the important parts. The notes have every line.",
        1: "Every lesson has companion notes in the repository.",
        2: "Every command, taken apart piece by piece",
        3: "Common errors, and how to recover",
        4: "Keep them open while you work.",
        5: "When the video moves fast, the detail is in the notes.",
    }[i]
    takeaway(d, text, y=800)
    return im


# Scene 9 — What you need
def scene9(i):
    im, d = canvas(HEADER)
    title(d, "What you need")
    cw = (W - 2 * MARGIN - 60) // 2
    cols = [
        ("You need", ["Python", "A terminal"], TEAL, tick),
        ("You don't need yet", ["Docker", "Django's advanced features"], AMBER, None),
    ]
    for k, (head, items, accent, mark) in enumerate(cols):
        if k > i:
            break
        x0 = MARGIN + k * (cw + 60)
        on = k == i or (i == 2 and k == 1)
        d.rounded_rectangle(
            (x0, 250, x0 + cw, 620),
            radius=22,
            fill=PANEL,
            outline=accent if on else DIM,
            width=5 if on else 2,
        )
        d.text((x0 + 44, 284), head, font=font(46, bold=True), fill=TEXT)
        for j, it in enumerate(items):
            y = 390 + j * 90
            if mark:
                mark(d, (x0 + 44, y + 6), size=36)
            else:
                d.text((x0 + 44, y - 4), "+", font=font(50, bold=True), fill=AMBER)
            d.text((x0 + 110, y), it, font=font(44), fill=TEXT if on else MUTED)
        if k == 1 and i >= 2:
            d.text(
                (x0 + 44, 560 - 10), "We'll build those up.", font=font(34), fill=AMBER
            )
    foot = {
        3: "Free tools only. The next lesson checks your machine has them.",
        4: "Short lessons, 10 to 15 minutes, built on each other.",
        5: "Watch in order. Type the commands yourself.",
    }.get(i)
    if foot:
        takeaway(d, foot, y=700)
    return im


# Scene 10 — Next
def scene10(i):
    im, d = canvas(HEADER)
    centered(d, 360, "Next", font(40), MUTED)
    centered(d, 430, "M0.2  ·  Your toolchain, verified", font(76, bold=True), TEXT)
    centered(
        d, 560, "One tool at a time, and what to do when a check fails", font(40), MUTED
    )
    return im


SCENES = {
    1: scene1,
    2: scene2,
    3: scene3,
    4: scene4,
    5: scene5,
    6: scene6,
    7: scene7,
    8: scene8,
    9: scene9,
    10: scene10,
}


def frame(scene, index):
    return SCENES[scene](index)
