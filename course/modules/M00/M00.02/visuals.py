"""M00.02 visuals: one picture per narrated sentence (see storyboard.md).

Terminal text is real output, captured 2026-11-08 on the recording Mac (macOS 26.6.2,
Docker Desktop 4.98.0 / Engine 29.9.2 / Compose 5.6.1, uv 0.13.7, git 2.50.1):
  scene 3: `git --version`; `git config user.email` inside this repository (the no-reply
           address). The global identity on the recording machine is never shown.
  scene 4: `uv --version`, `uv python install 3.14`, `uv python find 3.14`
  scene 5: `docker version` (the containerd/runc/docker-init blocks are cut, marked "…")
  scene 6: `docker version` after quitting Docker Desktop and waiting for it to exit fully
  scene 7: `docker run --rm hello-world` (first lines of the message)
  scene 8: `docker compose version`
  scene 10: `sh scripts/doctor.sh`, and the same with DOCKER_HOST=unix:///nonexistent.sock
Display edits, nothing else: the home folder is shown as "~" (or "/Users/…" inside a URL), and
long lines are clipped with "…".
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

HEADER = "M0.2  ·  Your toolchain, verified"
P = [("$ ", MUTED, False)]  # prompt


def cmd(text, hi=None):
    """A command line; `hi` is a substring to highlight."""
    if hi and hi in text:
        a, b = text.split(hi, 1)
        return P + [(a, TEXT, False), (hi, AMBER, True), (b, TEXT, False)]
    return P + [(text, TEXT, False)]


def out(text, col=TEXT, hi=False):
    return [(text, col, hi)]


# Scene 1 — Why verify
def scene1(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "Before any Django: is your machine ready?", y=400, size=64)
        return im
    title(d, "Installed is not the same as working")
    cw = 700
    card(
        d,
        (MARGIN, 300, MARGIN + cw, 560),
        "Installed",
        "The command exists.",
        on=i == 1,
        accent=TEAL,
    )
    card(
        d,
        (W - MARGIN - cw, 300, W - MARGIN, 560),
        "Working",
        "The command does its job.",
        on=i >= 1,
        accent=AMBER,
    )
    centered(d, 395, "≠", font(110, bold=True), AMBER)
    if i == 2:
        takeaway(d, "Find out now, not halfway through Module 1.", y=640)
    if i == 3:
        steps = ["Install it", "Run a check", "Know what failure looks like"]
        f = font(40, bold=True)
        x = MARGIN
        for k, s in enumerate(steps):
            d.rounded_rectangle(
                (x, 640, x + f.getlength(s) + 60, 720), radius=16, fill=PANEL
            )
            d.text((x + 30, 657), s, font=f, fill=TEXT)
            x += f.getlength(s) + 60
            if k < 2:
                arrow(d, (x + 20, 680), (x + 90, 680), fill=TEAL)
                x += 110
    return im


# Scene 2 — The four tools
TOOLS = [
    ("Git", "Track your code; follow the checkpoints"),
    ("uv", "Installs Python; manages dependencies"),
    ("Docker", "Runs the apps and databases in containers"),
    ("Compose", "Runs several containers from one file"),
]


def scene2(i):
    im, d = canvas(HEADER)
    title(d, "Four tools")
    gap = 30
    cw = (W - 2 * MARGIN - 3 * gap) // 4
    for k, (name, line) in enumerate(TOOLS):
        x0 = MARGIN + k * (cw + gap)
        card(
            d,
            (x0, 290, x0 + cw, 560),
            name,
            line,
            on=i == 0 or i >= 5 or k == i - 1,
            hsize=44,
            bsize=32,
        )
    if i >= 5:
        d.rounded_rectangle(
            (MARGIN, 620, W - MARGIN, 740),
            radius=22,
            fill=PANEL,
            outline=AMBER,
            width=4,
        )
        d.text(
            (MARGIN + 40, 646),
            "Plus a code editor",
            font=font(40, bold=True),
            fill=TEXT,
        )
        if i == 6:
            d.text(
                (MARGIN + 520, 652),
                "VS Code here; any editor that understands Python is fine",
                font=font(34),
                fill=MUTED,
            )
    return im


# Scene 3 — Git
def scene3(i):
    im, d = canvas(HEADER)
    title(d, "Git")
    lines = []
    if i >= 1:
        lines += [
            cmd("git --version"),
            out("git version 2.50.1 (Apple Git-155)", TEXT, i == 2),
        ]
    if i >= 3:
        lines += [
            "",
            cmd(
                'git config --global user.name "Your Name"',
                "--global" if i == 4 else None,
            ),
            cmd(
                "git config --global user.email 12345+you@users.noreply.github.com",
                "--global" if i == 4 else None,
            ),
        ]
    if i >= 5:
        lines += [
            "",
            out("# in the course repository: the address used to record it", MUTED),
            cmd("git config user.email"),
            out("26723770+iamyinka@users.noreply.github.com", TEAL, True),
        ]
    if lines:
        terminal(d, (MARGIN, 230, W - MARGIN, 700), lines, size=28)
    note = {
        2: "Version 2.40 or newer is fine.",
        3: "Your name and email go into every commit.",
        4: "--global: every repository on this machine (~/.gitconfig)",
        5: "Public repository? Use GitHub's no-reply email.",
    }.get(i)
    if note:
        takeaway(d, note, y=760)
    return im


# Scene 4 — uv and Python
def scene4(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "uv")
        paragraph(
            d,
            (MARGIN, 260),
            "Installs Python, and manages each project's dependencies.",
            font(44),
            TEXT,
            1600,
        )
        return im
    if i <= 3:
        title(d, "Installing uv")
        lines = [
            out(
                "# the one-line installer from the uv install page (docs.astral.sh/uv)",
                MUTED,
            ),
            cmd(
                "curl -LsSf https://astral.sh/uv/install.sh | sh",
                "| sh" if i >= 2 else None,
            ),
        ]
        if i == 3:
            lines += [
                "",
                out("# safer: download it, read it, then run it", MUTED),
                cmd("curl -LsSf -o uv-install.sh https://astral.sh/uv/install.sh"),
                cmd("less uv-install.sh"),
                cmd("sh uv-install.sh"),
                "",
                out("# or a package manager, e.g.  brew install uv", MUTED),
            ]
        terminal(d, (MARGIN, 230, W - MARGIN, 720 if i == 3 else 420), lines, size=28)
        if i == 2:
            takeaway(d, "Piping into sh runs whatever the server sends, unread.", y=520)
        return im
    if i <= 6:
        title(d, "Check uv, then ask it for Python 3.14")
        lines = [
            cmd("uv --version"),
            out("uv 0.13.7 (316c827e0 2026-11-03 aarch64-apple-darwin)"),
        ]
        if i >= 5:
            lines += [
                "",
                cmd("uv python install 3.14"),
                out(
                    "Downloading cpython-3.14.10-macos-aarch64-none (download) (25.5MiB)",
                    MUTED,
                ),
                out(" Downloaded cpython-3.14.10-macos-aarch64-none (download)", MUTED),
                out("Installed Python 3.14.10 in 1.35s", TEAL, i == 5),
                out(" + cpython-3.14.10-macos-aarch64-none (python3.14)", TEXT),
            ]
        if i == 6:
            lines += [
                "",
                cmd("uv python find 3.14"),
                out(
                    "~/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14",
                    AMBER,
                    True,
                ),
            ]
        terminal(d, (MARGIN, 230, W - MARGIN, 860), lines, size=26)
        return im
    # i 7..9: where Python runs
    title(d, "Where Python runs in this course")
    cw = (W - 2 * MARGIN - 60) // 2
    boxes = [
        (
            "Your machine",
            "Python 3.14 from uv",
            ["Running checks", "Formatting code", "Helping your editor"],
            i == 9,
            AMBER,
        ),
        (
            "Each app's container",
            "python:3.14.10-slim-trixie",
            [
                "Runs the Django apps",
                "Same Python for everyone",
                "Pinned in the Dockerfile",
            ],
            i == 8,
            TEAL,
        ),
    ]
    for k, (head, sub, items, on, accent) in enumerate(boxes):
        x0 = MARGIN + k * (cw + 60)
        d.rounded_rectangle(
            (x0, 270, x0 + cw, 700),
            radius=22,
            fill=PANEL,
            outline=accent if on else DIM,
            width=5 if on else 2,
        )
        d.text(
            (x0 + 40, 300),
            head,
            font=font(44, bold=True),
            fill=TEXT if on or i == 7 else MUTED,
        )
        d.text(
            (x0 + 40, 370), sub, font=font(30, mono=True), fill=accent if on else MUTED
        )
        for j, it in enumerate(items):
            d.text(
                (x0 + 40, 460 + j * 66),
                "•  " + it,
                font=font(36),
                fill=TEXT if on else MUTED,
            )
    takeaway(
        d,
        {
            7: "Two Pythons, two jobs.",
            8: "The apps run on the Python inside their images.",
            9: "The Python on your machine is for tools.",
        }[i],
        y=760,
    )
    return im


# Scene 5 — Docker has two halves
DV_CLIENT = [
    "Client:",
    " Version:           29.9.2",
    " API version:       1.56",
    " Go version:        go1.26.10",
    " Git commit:        a82e528",
    " Built:             Tue Oct 20 18:43:59 2026",
    " OS/Arch:           darwin/arm64",
    " Context:           desktop-linux",
]
DV_SERVER = [
    "Server: Docker Desktop 4.98.0 (245422)",
    " Engine:",
    "  Version:          29.9.2",
    "  API version:      1.56 (minimum version 1.40)",
    "  Go version:       go1.26.10",
    "  Git commit:       0367cbe",
    "  Built:            Tue Oct 20 18:44:14 2026",
    "  OS/Arch:          linux/arm64",
    "  Experimental:     false",
    " …  (containerd, runc, docker-init)",
]


def docker_version(d, box, client_on=True, server_on=True, server=True, size=22):
    lines = [cmd("docker version")]
    lines += [
        out(
            t,
            (TEAL if t == "Client:" else TEXT) if client_on else MUTED,
            t == "Client:" and client_on,
        )
        for t in DV_CLIENT
    ]
    if server:
        lines += [""] + [
            out(
                t,
                (TEAL if t.startswith("Server") else TEXT) if server_on else MUTED,
                t.startswith("Server") and server_on,
            )
            for t in DV_SERVER
        ]
    return terminal(d, box, lines, size=size)


def scene5(i):
    im, d = canvas(HEADER)
    if i <= 2:
        title(d, "Installing Docker")
        cw = (W - 2 * MARGIN - 60) // 2
        card(
            d,
            (MARGIN, 290, MARGIN + cw, 560),
            "macOS and Windows",
            "Docker Desktop",
            on=i in (0, 1),
            hsize=44,
            bsize=36,
        )
        card(
            d,
            (MARGIN + cw + 60, 290, W - MARGIN, 560),
            "Linux",
            "Docker Engine from Docker's own repository, not your distribution's old package",
            on=i in (0, 2),
            hsize=44,
            bsize=36,
        )
        return im
    if i <= 6:
        docker_version(
            d,
            (MARGIN, 110, 1150, 900),
            client_on=i in (3, 4, 5),
            server_on=i in (3, 4, 6),
        )
        x = 1210
        notes = {
            3: [("Two sections:", TEXT)],
            4: [("Two sections:", TEXT), ("Client", TEAL), ("Server", TEAL)],
            5: [("Client", TEAL), ("the docker command you type", TEXT)],
            6: [
                ("Server", TEAL),
                ("the Docker daemon: builds", TEXT),
                ("images and runs containers", TEXT),
            ],
        }[i]
        y = 240
        for t, c in notes:
            d.text(
                (x, y), t, font=font(44 if c == TEAL else 38, bold=c == TEAL), fill=c
            )
            y += 70
        return im
    # i 7, 8: where the daemon lives on a Mac
    title(d, "On a Mac, the daemon runs in a Linux VM")
    host = (MARGIN, 260, W - MARGIN, 760)
    d.rounded_rectangle(host, radius=26, outline=DIM, width=3)
    d.text((MARGIN + 30, 280), "Your Mac (macOS)", font=font(34, bold=True), fill=MUTED)
    card(
        d,
        (MARGIN + 60, 400, MARGIN + 560, 640),
        "docker CLI",
        "The client: what you type",
        hsize=40,
        bsize=32,
    )
    vm = (900, 340, W - MARGIN - 40, 720)
    d.rounded_rectangle(vm, radius=22, fill=PANEL, outline=TEAL, width=5)
    d.text(
        (940, 365),
        "Linux VM, managed by Docker Desktop",
        font=font(32, bold=True),
        fill=TEAL,
    )
    d.text((940, 440), "Docker daemon (the server)", font=font(36), fill=TEXT)
    for k in range(3):
        bx = 940 + k * 270
        d.rounded_rectangle(
            (bx, 520, bx + 240, 660),
            radius=14,
            outline=AMBER if i == 8 else DIM,
            width=3,
        )
        d.text((bx + 24, 545), "container", font=font(28), fill=TEXT)
        d.text(
            (bx + 24, 595),
            "Linux",
            font=font(28, bold=True),
            fill=AMBER if i == 8 else MUTED,
        )
    arrow(d, (MARGIN + 570, 520), (890, 520), fill=TEAL)
    if i == 8:
        takeaway(d, "A container on your Mac runs Linux, not macOS.", y=800)
    return im


# Scene 6 — A real failure
ERR = (
    "failed to connect to the docker API at unix:///Users/…/.docker/run/docker.sock; "
    "check if the path is correct and if the daemon is running: dial unix /Users/…/.docker/run/docker.sock: "
    "connect: no such file or directory"
)


def wrap_mono(text, width_chars):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width_chars:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


def scene6(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "The failure you're most likely to see", y=400, size=64)
        return im
    if i <= 5:
        lines = [
            out("# Docker Desktop quit, and fully stopped", MUTED),
            cmd("docker version"),
        ]
        lines += [
            out(t, TEAL if i == 2 else TEXT, i == 2 and t == "Client:")
            for t in DV_CLIENT
        ]
        lines += [out(t, RED, i == 3) for t in wrap_mono(ERR, 74)]
        bottom = terminal(d, (MARGIN, 110, 1360, 800), lines, size=22)
        x = 1420
        if i >= 4:
            tick(d, (x, 300), size=40)
            d.text((x + 64, 296), "installed", font=font(40), fill=TEXT)
        if i >= 5:
            cross(d, (x + 4, 404), size=34)
            d.text((x + 64, 396), "running", font=font(40), fill=TEXT)
            paragraph(
                d,
                (x, 500),
                "Nothing can run: the server isn't there.",
                font(34),
                AMBER,
                400,
            )
        del bottom
        return im
    if i <= 7:
        title(d, "The fix")
        cw = (W - 2 * MARGIN - 60) // 2
        card(
            d,
            (MARGIN, 270, MARGIN + cw, 520),
            "macOS and Windows",
            "Start Docker Desktop",
            hsize=42,
            bsize=36,
        )
        card(
            d,
            (MARGIN + cw + 60, 270, W - MARGIN, 520),
            "Linux",
            "sudo systemctl start docker",
            hsize=42,
            bsize=36,
        )
        if i == 7:
            takeaway(d, "Wait until it says it's running, then check again.", y=600)
        return im
    docker_version(d, (MARGIN, 110, 1150, 900))
    d.text((1210, 260), "Both halves answer.", font=font(44, bold=True), fill=TEAL)
    return im


# Scene 7 — Prove a container runs
HELLO = [
    "Unable to find image 'hello-world:latest' locally",
    "latest: Pulling from library/hello-world",
    "…",
    "Status: Downloaded newer image for hello-world:latest",
    "",
    "Hello from Docker!",
    "This message shows that your installation appears to be working correctly.",
    "",
    "To generate this message, Docker took the following steps:",
    " 1. The Docker client contacted the Docker daemon.",
    ' 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.',
    " 3. The Docker daemon created a new container from that image which runs the",
    "    executable that produces the output you are currently reading.",
    " 4. The Docker daemon streamed that output to the Docker client, which sent it",
    "    to your terminal.",
]


def scene7(i):
    im, d = canvas(HEADER)
    if i == 0:
        title(d, "A reachable daemon still isn't the whole story", y=400, size=60)
        return im
    lines = [cmd("docker run --rm hello-world", "--rm" if i == 3 else None)]
    if i >= 2:
        lines += [
            out(
                t,
                TEAL if t.startswith("Hello") else (MUTED if k < 4 else TEXT),
                t.startswith("Hello"),
            )
            for k, t in enumerate(HELLO)
        ]
    terminal(d, (MARGIN, 110, W - MARGIN, 760), lines, size=24)
    text = {
        1: "Run a real container.",
        2: "Pull an image, start a container, print, exit.",
        3: "--rm deletes the stopped container afterwards.",
        4: "Images download, containers run: all Module 1 needs.",
    }[i]
    takeaway(d, text, y=800)
    return im


# Scene 8 — Compose
def scene8(i):
    im, d = canvas(HEADER)
    title(d, "Compose")
    lines = (
        [cmd("docker compose version", " compose " if i == 1 else None)]
        if i >= 1
        else [cmd("docker compose version")]
    )
    lines += [out("Docker Compose version v5.6.1", TEAL)]
    terminal(d, (MARGIN, 240, W - MARGIN, 420), lines, size=32)
    if i == 0:
        takeaway(d, "Included with Docker Desktop; a plugin on Linux.", y=500)
    if i >= 2:
        y = 500
        f = font(44, mono=True)
        d.text((MARGIN, y), "docker-compose", font=f, fill=MUTED)
        w = f.getlength("docker-compose")
        d.line((MARGIN - 6, y + 28, MARGIN + w + 6, y + 28), fill=RED, width=5)
        if i >= 3:
            d.text(
                (MARGIN + w + 50, y + 4),
                "the retired standalone program",
                font=font(40),
                fill=MUTED,
            )
        if i == 4:
            d.text((MARGIN, y + 110), "docker compose", font=f, fill=TEAL)
            d.text(
                (MARGIN + w + 50, y + 114),
                "the plugin: always, in this course",
                font=font(40),
                fill=TEXT,
            )
    return im


# Scene 9 — Platform notes
PLATFORMS = [
    (
        "Linux",
        ["docker group = root-equivalent", "Only on a machine you control"],
        (1, 2, 3),
    ),
    (
        "Windows (WSL 2)",
        ["Code under ~ in Linux", "Not under /mnt/c: very slow"],
        (4, 5),
    ),
    (
        "Every platform",
        ["Docker memory: 4 GB or more", "8 GB for later modules"],
        (6, 7),
    ),
]


def scene9(i):
    im, d = canvas(HEADER)
    title(d, "Platform notes")
    gap = 40
    cw = (W - 2 * MARGIN - 2 * gap) // 3
    for k, (head, items, active) in enumerate(PLATFORMS):
        x0 = MARGIN + k * (cw + gap)
        on = i in active
        seen = i >= active[0]
        d.rounded_rectangle(
            (x0, 260, x0 + cw, 700),
            radius=22,
            fill=PANEL,
            outline=AMBER if on else DIM,
            width=5 if on else 2,
        )
        d.text(
            (x0 + 36, 290),
            head,
            font=font(44, bold=True),
            fill=TEXT if on or i == 0 else MUTED,
        )
        if seen:
            y = 380
            for it in items:
                y = (
                    paragraph(
                        d, (x0 + 36, y), it, font(36), TEXT if on else MUTED, cw - 72
                    )
                    + 24
                )
    return im


# Scene 10 — One command for all of it
OK_LINES = [
    "git 2.50.1",
    "git identity: Abiola Oyewole <26723770+iamyinka@users.noreply.github.com>",
    "uv 0.13.7",
    "Python 3.14 available to uv (~/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14)",
    "docker CLI 29.9.2",
    "docker daemon 29.9.2 is reachable",
    "docker can pull and run a container (hello-world)",
    "docker compose 5.6.1 (the 'docker compose' plugin, not the old 'docker-compose')",
]


def doctor(fail=False, hi_last=False):
    lines = [out("Course toolchain check")]
    for t in OK_LINES:
        if fail and t.startswith("docker daemon"):
            lines.append(
                [("  FAIL  ", RED, True), ("docker daemon not reachable", TEXT, False)]
            )
            lines.append(
                out(
                    "        fix: start Docker Desktop (macOS/Windows) or 'sudo systemctl start docker' (Linux)",
                    AMBER,
                )
            )
            continue
        if fail and t.startswith("docker can pull"):
            continue  # the script skips this check when the daemon is unreachable
        lines.append([("  ok    ", TEAL, False), (t, TEXT, False)])
    lines.append("")
    lines.append(
        out(
            "Some checks failed. Fix them in order, then run this again."
            if fail
            else "All required checks passed.",
            RED if fail else TEAL,
            hi_last,
        )
    )
    return lines


def scene10(i):
    im, d = canvas(HEADER)
    if i <= 1:
        title(d, "One command for all of it")
        if i == 1:
            paragraph(
                d,
                (MARGIN, 260),
                "scripts/doctor.sh runs every check, in order.",
                font(44),
                TEXT,
                1600,
            )
        return im
    if i <= 3:
        terminal(
            d, (MARGIN, 200, W - MARGIN, 380), [cmd("sh scripts/doctor.sh")], size=30
        )
        if i == 3:
            takeaway(
                d, "Read-only: version commands and one throwaway container.", y=460
            )
        return im
    fail = i in (5, 6)
    lines = (
        [
            out("# Simulated failure: DOCKER_HOST points nowhere", AMBER),
            cmd("DOCKER_HOST=unix:///nonexistent.sock sh scripts/doctor.sh"),
        ]
        if fail
        else [cmd("sh scripts/doctor.sh")]
    )
    terminal(
        d, (MARGIN, 110, W - MARGIN, 720), lines + doctor(fail, hi_last=i == 7), size=22
    )
    if fail:
        badge(d, (MARGIN, 760), "Simulated", size=34)
    text = {
        4: "Each line: ok, or FAIL with the fix underneath.",
        5: "Fix from the top down: later checks depend on earlier ones.",
        6: "Run it again whenever something feels off.",
        7: "Every line ok: you're ready.",
    }[i]
    takeaway(d, text, y=780 if not fail else 840)
    return im


# Scene 11 — Next
def scene11(i):
    im, d = canvas(HEADER)
    centered(d, 360, "Next", font(40), MUTED)
    centered(
        d,
        430,
        "M0.3  ·  One repository, five independent apps",
        font(70, bold=True),
        TEXT,
    )
    centered(
        d,
        560,
        "How it's organized, and the files that must never be committed",
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
    11: scene11,
}


def frame(scene, index):
    return SCENES[scene](index)
