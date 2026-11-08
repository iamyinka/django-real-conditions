"""M00.03 visuals: one picture per narrated sentence (see storyboard.md).

Everything shown is real, captured 2026-11-08 in a clean worktree at lesson/M00.03-end:
  scenes 1, 3: the file tree (`ls -A`); scenes 5, 9: .gitignore, .gitattributes, .editorconfig
  scene 6: the cp / git status / git check-ignore commands and their output
  scene 7: a fake token generated with the storyboard's command, then
           `uvx pre-commit@4.7.0 run gitleaks --files projects/leak_demo.py` (exit 1).
           The gitleaks banner is cut ("…"). The token is stored split in two below, so this
           file doesn't trip the repository's own secret scanning.
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
    font,
    paragraph,
    takeaway,
    terminal,
    title,
)

HEADER = "M0.3  ·  One repository, five independent apps"
P = [("$ ", MUTED, False)]


def cmd(text, hi=None):
    if hi and hi in text:
        a, b = text.split(hi, 1)
        return P + [(a, TEXT, False), (hi, AMBER, True), (b, TEXT, False)]
    return P + [(text, TEXT, False)]


def out(text, col=TEXT, hi=False):
    return [(text, col, hi)]


def tree(d, box, rows, label="django-real-conditions"):
    """rows: (indent, name, state) with state 'on' | 'dim' | 'normal'."""
    lines = []
    for indent, name, state in rows:
        col = {"on": AMBER, "dim": MUTED, "normal": TEXT}[state]
        lines.append([("  " * indent + name, col, state == "on")])
    return terminal(d, box, lines, size=28, label=label)


# Scene 1 — The top level
TOP = [
    ".github/",
    "course/",
    "docs/",
    "projects/",
    "scripts/",
    "tools/",
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".pre-commit-config.yaml",
    "README.md",
]
FOLDERS = {
    2: (["projects/"], "projects/", ["telecom/   (the other four arrive later)"]),
    3: (
        ["course/"],
        "course/",
        ["modules/   scripts, notes, exercises", "OUTLINE.md", "style/", "VERSIONS.md"],
    ),
    4: (["docs/"], "docs/", ["GIT_WORKFLOW.md   the loop, protected main, review"]),
    5: (
        ["scripts/", "tools/"],
        "scripts/  ·  tools/",
        ["scripts/doctor.sh", "tools/stack-check/", "tools/course/"],
    ),
    6: (
        [".github/"],
        ".github/",
        [
            "pull_request_template.md",
            "ISSUE_TEMPLATE/  (issue forms)",
            "workflows/repo-checks.yml  (CI)",
        ],
    ),
}


def scene1(i):
    im, d = canvas(HEADER)
    hot = (
        FOLDERS[i][0]
        if i in FOLDERS
        else ([n for n in TOP if n.endswith("/")] if i == 1 else [])
    )
    rows = [(0, n, "on" if n in hot else ("dim" if hot else "normal")) for n in TOP]
    tree(d, (MARGIN, 110, 760, 760), rows)
    x = 840
    if i == 0:
        paragraph(
            d,
            (x, 260),
            "The top level of the course repository",
            font(48, bold=True),
            TEXT,
            980,
        )
    elif i == 1:
        paragraph(
            d, (x, 260), "Five folders that matter", font(48, bold=True), TEXT, 980
        )
    else:
        _, head, items = FOLDERS[i]
        d.text((x, 240), head, font=font(52, mono=True), fill=AMBER)
        for k, it in enumerate(items):
            d.text((x, 350 + k * 70), it, font=font(32, mono=True), fill=TEXT)
    return im


# Scene 2 — Why one repository
def scene2(i):
    im, d = canvas(HEADER)
    if i >= 4:
        centered(d, 360, "One repository", font(80, bold=True), TEXT)
        centered(d, 470, "≠", font(90, bold=True), AMBER)
        centered(d, 580, "one application", font(80, bold=True), TEXT)
        if i == 5:
            takeaway(d, "That distinction drives the whole layout.", y=740)
        return im
    title(d, "Why one repository?")
    if i >= 1:
        x = MARGIN
        for k, t in enumerate(
            ["One clone", "One history", "One set of checkpoint tags"]
        ):
            f = font(42, bold=True)
            w = f.getlength(t) + 70
            d.rounded_rectangle(
                (x, 290, x + w, 380),
                radius=20,
                fill=PANEL,
                outline=TEAL if i == 1 else DIM,
                width=4 if i == 1 else 2,
            )
            d.text((x + 35, 312), t, font=f, fill=TEXT)
            x += w + 30
    if i >= 2:
        d.text((MARGIN, 450), "Teams do it too: a", font=font(44), fill=TEXT)
        d.text(
            (MARGIN + font(44).getlength("Teams do it too: a "), 446),
            "monorepo",
            font=font(48, bold=True),
            fill=AMBER,
        )
    if i >= 3:
        d.text(
            (MARGIN, 560),
            "A change across several projects: one pull request to review.",
            font=font(44),
            fill=TEXT,
        )
    return im


# Scene 3 — Independent projects
TELECOM = [
    ".dockerignore",
    ".env.example",
    "compose.yaml",
    "config/",
    "core/",
    "Dockerfile",
    "manage.py",
    "pyproject.toml",
    "README.md",
    "tests/",
    "uv.lock",
]
OWN = {"pyproject.toml", "uv.lock", "Dockerfile", "compose.yaml"}


def scene3(i):
    im, d = canvas(HEADER)
    rows = [(0, "projects/", "normal"), (1, "telecom/", "normal")]
    rows += [
        (2, n, "on" if (n in OWN and i >= 1) else ("dim" if i >= 1 else "normal"))
        for n in TELECOM
    ]
    if i >= 2:
        rows += [
            (1, f"{p}/   later", "dim")
            for p in ("telehealth", "streaming", "labtrack", "intranet")
        ]
    tree(d, (MARGIN, 110, 820, 920), rows)
    x = 900
    if i == 1:
        for k, (f, why) in enumerate(
            [
                ("pyproject.toml", "its dependency list"),
                ("uv.lock", "its lock file"),
                ("Dockerfile", "its image"),
                ("compose.yaml", "its services"),
            ]
        ):
            d.text((x, 250 + k * 90), f, font=font(36, mono=True), fill=AMBER)
            d.text((x + 380, 254 + k * 90), why, font=font(34), fill=TEXT)
    if i == 2:
        paragraph(
            d,
            (x, 260),
            "Each project gets the same set.",
            font(44, bold=True),
            TEXT,
            900,
        )
    if i == 3:
        paragraph(
            d,
            (x, 260),
            "Start, stop, upgrade or delete one project without touching the others.",
            font(44),
            TEXT,
            900,
        )
    if i == 4:
        card(
            d,
            (x, 250, x + 420, 500),
            "telehealth",
            "moves to a newer library",
            accent=AMBER,
        )
        card(d, (x + 460, 250, x + 880, 500), "telecom", "stays put", accent=TEAL)
    if i == 5:
        d.text((x, 260), "Its own release tags:", font=font(44), fill=TEXT)
        d.rounded_rectangle(
            (x, 350, x + 520, 450), radius=18, fill=PANEL, outline=AMBER, width=4
        )
        d.text((x + 36, 372), "telecom/v1.0.0", font=font(46, mono=True), fill=AMBER)
    return im


# Scene 4 — Shared code stays small
NAMES = ["telecom", "telehealth", "streaming", "labtrack", "intranet"]


def scene4(i):
    im, d = canvas(HEADER)
    title(
        d,
        {0: "Where does shared code go?", 1: "Mostly, nowhere."}.get(
            i, "Copy small things"
        ),
    )
    gap = 30
    cw = (W - 2 * MARGIN - 4 * gap) // 5
    top = 520
    shared = i in (4, 5, 6)
    broken = i in (5, 6)
    for k, n in enumerate(NAMES):
        x0 = MARGIN + k * (cw + gap)
        red = broken
        d.rounded_rectangle(
            (x0, top, x0 + cw, top + 200),
            radius=20,
            fill=PANEL,
            outline=RED if red else (TEAL if i >= 2 else DIM),
            width=4 if i >= 2 else 2,
        )
        d.text((x0 + 26, top + 26), n, font=font(34, bold=True), fill=TEXT)
        if i >= 2 and not shared:
            d.rounded_rectangle(
                (x0 + 26, top + 110, x0 + 206, top + 166),
                radius=10,
                fill="#0b1120",
                outline=DIM,
            )
            d.text(
                (x0 + 42, top + 120), "healthz", font=font(26, mono=True), fill=AMBER
            )
    if shared:
        sx0, sx1 = W // 2 - 300, W // 2 + 300
        d.rounded_rectangle(
            (sx0, 270, sx1, 380),
            radius=18,
            fill=PANEL,
            outline=RED if broken else AMBER,
            width=5,
        )
        centered(
            d,
            296,
            "shared/ (changed for one)" if broken else "shared/",
            font(38, bold=True),
            RED if broken else AMBER,
        )
        for k in range(5):
            cx = MARGIN + k * (cw + gap) + cw // 2
            arrow(
                d,
                (W // 2, 384),
                (cx, top - 8),
                fill=RED if broken else AMBER,
                width=4,
                head=16,
            )
    caption = {
        2: "Each project gets its own small copy.",
        3: "Sounds wasteful. Sometimes it is.",
        4: "Shared code couples projects together…",
        5: "…change it for one, you've changed it for all five.",
        6: "At work: one team's change breaks another team's deploy.",
        7: "Share only when duplication clearly costs more than coupling.",
    }.get(i)
    if caption:
        takeaway(d, caption, y=790)
    return im


# Scene 5 — What never gets committed
SECTIONS = {
    1: [
        "# --- Secrets and local configuration: never commit ---",
        ".env",
        ".env.*",
        "!.env.example",
        "*.pem",
        "*.key",
        "*.p12",
        "*.ovpn",
        "pki/",
        "secrets/",
    ],
    2: [
        "# --- Databases, uploaded media, generated files ---",
        "*.sqlite3",
        "*.db",
        "media/",
        "staticfiles/",
        "*.dump",
        "*.sql.gz",
        "backups/",
    ],
    4: [
        "# --- Local environments ---",
        ".venv/",
        "venv/",
        "__pycache__/",
        "*.py[cod]",
        ".python-version",
    ],
    5: [
        "# --- Rendered course media: stored outside Git (checksums are committed) ---",
        "*.mp4",
        "*.webm",
        "*.mov",
        "*.wav",
        "*.mp3",
        "*.m4a",
        "course/**/render/",
    ],
}
SECTIONS[3] = SECTIONS[2]
FOCUS = {2: {"*.sqlite3", "*.db", "*.dump", "*.sql.gz", "backups/"}, 3: {"media/"}}
ITEMS = [
    "Secrets",
    "Local databases",
    "Uploaded media",
    "Virtual environments",
    "Rendered videos",
]


def scene5(i):
    im, d = canvas(HEADER)
    title(d, "Never committed")
    for k, it in enumerate(ITEMS):
        if k >= i:
            break
        on = k == i - 1 or i == 6
        d.text(
            (MARGIN, 270 + k * 90),
            it,
            font=font(44, bold=on),
            fill=TEXT if on else MUTED,
        )
    if i in SECTIONS:
        focus = FOCUS.get(i)
        lines = [
            out(
                t,
                TEAL
                if t.startswith("#")
                else (AMBER if focus and t in focus else TEXT),
                bool(focus and t in focus),
            )
            for t in SECTIONS[i]
        ]
        terminal(d, (760, 230, W - MARGIN, 760), lines, size=26, label=".gitignore")
    if i == 6:
        lines = [
            out(h, TEAL, True)
            for h in (
                "# --- Secrets and local configuration: never commit ---",
                "# --- Local environments ---",
                "# --- Databases, uploaded media, generated files ---",
                "# --- Rendered course media: stored outside Git ---",
                "# --- Tool caches ---",
                "# --- Editors and OS ---",
            )
        ]
        terminal(
            d,
            (760, 230, W - MARGIN, 640),
            lines,
            size=26,
            label=".gitignore  (repository root)",
        )
    return im


# Scene 6 — Proving the ignore rules
def scene6(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "Don't trust an ignore file. Test it.", y=400, size=64)
        return im
    L = []
    if i >= 1:
        L += [cmd("cp projects/telecom/.env.example projects/telecom/.env")]
    if i >= 2:
        L += [cmd("git status")]
    if i >= 3:
        L += [
            out("Not currently on any branch."),
            out("nothing to commit, working tree clean", TEAL, i == 3),
        ]
    if i >= 4:
        L += [
            cmd("git check-ignore -v projects/telecom/.env", "-v" if i == 4 else None)
        ]
    if i >= 5:
        L += [
            [
                (".gitignore:2:.env", AMBER, i == 5),
                ("\tprojects/telecom/.env", TEXT, False),
            ]
        ]
    if i >= 6:
        L += [cmd("git check-ignore -v projects/telecom/.env.example")]
    if i >= 7:
        L += [out("(no output)", MUTED, i == 7)]
    if i >= 10:
        L += [
            cmd(
                "git check-ignore -v --no-index projects/telecom/.env.example",
                "--no-index",
            )
        ]
    if i >= 11:
        L += [
            [
                (".gitignore:4:", TEXT, False),
                ("!.env.example", AMBER, i == 11),
                ("    projects/telecom/.env.example", TEXT, False),
            ]
        ]
    terminal(d, (MARGIN, 110, W - MARGIN, 640), L, size=26)
    note = {
        1: "A .env file: the kind that holds real secrets",
        3: "It doesn't appear.",
        4: "Why? Ask Git which rule matched.",
        5: "The exact rule, and its line in .gitignore",
        7: "Nothing prints.",
        8: ".env.example is tracked: ignore rules never apply to tracked files.",
        9: "Adding a rule doesn't un-commit anything.",
        10: "--no-index: test the rules alone",
        11: "!  marks an exception: keep this file out of the ignore list.",
        12: "Committed on purpose, with a harmless placeholder for every setting.",
    }.get(i)
    if note:
        takeaway(d, note, y=700)
    return im


# Scene 7 — When a secret slips through
FAKE = (
    "gh" + "p_" + "aJ50nEaJKnMiw30uYe3JLKeQOeazOulgiqSW"
)  # fake, generated for the demo
GITLEAKS = [
    "Detect hardcoded secrets.................................................Failed",
    "- hook id: gitleaks",
    "- exit code: 1",
    "…",
    "Finding:     GITHUB_TOKEN=REDACTED",
    "Secret:      REDACTED",
    "RuleID:      github-pat",
    "Entropy:     4.565311",
    "File:        projects/leak_demo.py",
    "Line:        1",
    "Fingerprint: projects/leak_demo.py:github-pat:1",
    "WRN leaks found: 1",
]
HOT = ("Detect", "RuleID", "File", "Line")


def scene7(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "Ignore rules only cover files you planned for", y=400, size=60)
        return im
    if i <= 2:
        title(d, "A token pasted into a file")
        terminal(
            d,
            (MARGIN, 260, W - MARGIN, 400),
            [out(f"GITHUB_TOKEN={FAKE}", AMBER, i == 2)],
            size=34,
            label="projects/leak_demo.py",
        )
        badge(d, (MARGIN, 460), "Simulated", size=34)
        if i == 2:
            d.text(
                (MARGIN + 290, 470),
                "Fake, generated for this demo, in the shape of a GitHub token",
                font=font(36),
                fill=TEXT,
            )
        return im
    if i <= 5:
        L = [
            cmd("git add projects/leak_demo.py"),
            cmd("uvx pre-commit@4.7.0 run gitleaks --files projects/leak_demo.py"),
        ]
        if i >= 4:
            L += [
                out(
                    t,
                    RED
                    if t.startswith("Detect")
                    else (TEXT if t.startswith(HOT) else MUTED),
                    i == 4 and t.startswith(HOT),
                )
                for t in GITLEAKS
            ]
        terminal(d, (MARGIN, 110, W - MARGIN, 780), L, size=24)
        badge(d, (MARGIN, 810), "Simulated", size=30)
        if i == 5:
            d.text(
                (MARGIN + 260, 818),
                "Exit code 1: the commit doesn't happen.",
                font=font(38),
                fill=TEXT,
            )
        return im
    title(d, "The same scanner, twice")
    card(
        d,
        (MARGIN, 290, MARGIN + 760, 580),
        "On every commit",
        "pre-commit runs gitleaks locally",
    )
    card(
        d,
        (W - MARGIN - 760, 290, W - MARGIN, 580),
        "In CI",
        "repo-checks.yml runs it again, in case the local hooks were skipped",
        accent=AMBER,
    )
    arrow(d, (MARGIN + 790, 435), (W - MARGIN - 790, 435), fill=TEAL)
    return im


# Scene 8 — Why "just delete it" isn't enough
def scene8(i):
    im, d = canvas(HEADER)
    title(d, "Why “just delete it” isn't enough")
    y = 420
    nodes = [
        ("commit A", "adds the secret", RED),
        ("commit B", "deletes the file", TEXT),
    ]
    if i >= 2:
        nodes.append(("any clone", "still has commit A", RED))
    if i >= 1:
        x = MARGIN
        for k, (n, sub, col) in enumerate(nodes):
            d.ellipse((x, y, x + 60, y + 60), fill=PANEL, outline=col, width=5)
            d.text((x - 10, y + 90), n, font=font(36, bold=True), fill=TEXT)
            d.text(
                (x - 10, y + 140), sub, font=font(32), fill=col if col == RED else MUTED
            )
            if k < len(nodes) - 1:
                arrow(
                    d,
                    (x + 70, y + 30),
                    (x + 460, y + 30),
                    fill=DIM if k == 0 else AMBER,
                )
            x += 540
    text = {
        3: "Public repository: automated scanners find leaked keys within minutes.",
        4: "The real fix: revoke the secret, issue a new one.",
        5: "Rewriting history comes second. It can't reach existing copies.",
    }.get(i)
    if text:
        takeaway(d, text, y=760)
    return im


# Scene 9 — Line endings and editor settings
ATTR = [
    "# Normalize line endings so Windows checkouts don't break shell scripts or Dockerfiles.",
    "* text=auto eol=lf",
    "*.sh text eol=lf",
    "*.png binary",
    "*.jpg binary",
    "*.svg text",
]
EDITOR = [
    "root = true",
    "",
    "[*]",
    "charset = utf-8",
    "end_of_line = lf",
    "insert_final_newline = true",
    "trim_trailing_whitespace = true",
    "indent_style = space",
    "indent_size = 4",
    "",
    "[*.{yml,yaml,json,toml,html,css,js}]",
    "indent_size = 2",
]


def scene9(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "Two more small files at the root")
        for k, n in enumerate([".gitattributes", ".editorconfig"]):
            d.text((MARGIN, 300 + k * 100), n, font=font(52, mono=True), fill=AMBER)
        return im
    if i <= 2:
        L = [
            out(
                t,
                AMBER
                if t == "* text=auto eol=lf"
                else (MUTED if t.startswith("#") else TEXT),
                t == "* text=auto eol=lf",
            )
            for t in ATTR
        ]
        terminal(d, (MARGIN, 110, W - MARGIN, 470), L, size=28, label=".gitattributes")
        takeaway(
            d,
            "Text files are stored with Unix line endings (LF)."
            if i == 1
            else "Otherwise: hidden carriage returns (\\r) break shell scripts in Linux containers.",
            y=540,
        )
        return im
    L = [
        out(
            t,
            AMBER if t in ("insert_final_newline = true", "indent_size = 4") else TEXT,
            t in ("insert_final_newline = true", "indent_size = 4"),
        )
        for t in EDITOR
    ]
    terminal(d, (MARGIN, 110, W - MARGIN, 640), L, size=26, label=".editorconfig")
    takeaway(
        d, "Same indentation and final newline in every editor: clean diffs.", y=700
    )
    return im


# Scene 10 — Next
def scene10(i):
    im, d = canvas(HEADER)
    centered(d, 360, "Next", font(40), MUTED)
    centered(d, 430, "M0.4  ·  The professional Git loop", font(76, bold=True), TEXT)
    centered(
        d,
        560,
        "Issue, branch, commits, pull request, review, merge, tags",
        font(40),
        MUTED,
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
