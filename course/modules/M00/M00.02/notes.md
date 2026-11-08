# Notes — M00.02 Your toolchain, verified

Versions used to record the course are in [`course/VERSIONS.md`](../../../VERSIONS.md). Newer patch versions of these tools are fine.

## Install

| Tool | macOS | Linux | Windows |
|---|---|---|---|
| Git | Comes with Xcode Command Line Tools (`xcode-select --install`) or Homebrew (`brew install git`) | Your package manager (`sudo apt install git`) | Inside WSL2: `sudo apt install git` |
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh`, or `brew install uv` | Same installer, or your package manager | Inside WSL2: the same installer |
| Python 3.14 | `uv python install 3.14` | same | same (inside WSL2) |
| Docker + Compose | Docker Desktop | Docker Engine + `docker-compose-plugin` from Docker's apt/dnf repository | Docker Desktop with the WSL2 backend |

**WSL2:** run every course command inside your Linux distribution, and keep the repository under `~` (for example `~/code/django-real-conditions`), not under `/mnt/c/...`.

## Commands

### `git --version`
- **Where it runs:** host
- **Expected output:** `git version 2.50.1` (any version ≥ 2.40)

### `git config --global user.name "Your Name"` / `git config --global user.email you@example.com`

| Part | Meaning |
|---|---|
| `git config` | Read or write Git settings |
| `--global` | Write to `~/.gitconfig`, so it applies to every repository for this user. Without it, the setting applies only to the current repository (`.git/config`). |
| `user.name` / `user.email` | Recorded as the author of every commit you make |

- **Side effects:** edits `~/.gitconfig`.
- **Public repositories:** use GitHub's no-reply address (Settings → Emails → "Keep my email addresses private"). It looks like `12345+you@users.noreply.github.com`. The email you commit with is published in the history forever.

### `curl -LsSf https://astral.sh/uv/install.sh | sh`

| Part | Meaning |
|---|---|
| `curl` | Downloads a URL |
| `-L` | Follow redirects |
| `-s` | Silent: no progress bar |
| `-S` | …but still show errors |
| `-f` | Fail on HTTP errors instead of piping an error page into the shell |
| `\| sh` | Pipe the downloaded script into a shell, which runs it immediately |

- **Why be careful:** you run whatever the server sends, without reading it. The safer variant: `curl -LsSf -o uv-install.sh https://astral.sh/uv/install.sh`, read it, then `sh uv-install.sh`.
- **Side effects:** installs `uv` and `uvx` into `~/.local/bin` and may add that to your shell's `PATH`. Open a new terminal afterwards.

### `uv python install 3.14` and `uv python find 3.14`
- **Where it runs:** host
- `install` downloads a standalone CPython build into uv's own directory. It doesn't touch the system Python.
- `find` prints the path of a matching interpreter, or fails if there isn't one.
- **Where Python runs in this course:** apps run on the Python inside their Docker image (`python:3.14.10-slim-trixie`). Host Python runs only tools.

### `docker version`

| Section | What it describes |
|---|---|
| `Client` | The `docker` CLI you typed |
| `Server` | The Docker daemon (`dockerd`) that builds images and runs containers. On macOS and Windows it runs inside a Linux VM managed by Docker Desktop. |

- **If it fails:** `Cannot connect to the Docker daemon at unix:///…/docker.sock. Is the docker daemon running?` means the client works but the daemon isn't reachable. Start Docker Desktop, or on Linux run `sudo systemctl start docker` (and `sudo systemctl enable docker` to start it at boot).

### `docker run --rm hello-world`

| Part | Meaning |
|---|---|
| `docker run` | Create a container from an image and start it. The image is pulled first if it isn't local. |
| `--rm` | Delete the container when it exits |
| `hello-world` | Short for `docker.io/library/hello-world:latest` |

- **Expected output:** `Hello from Docker!` followed by an explanation of the steps that just happened.
- **If it fails:** a pull error usually means no network access to Docker Hub, or a proxy.

### `docker compose version`
- **Expected output:** `Docker Compose version v5.1.1`
- `docker compose` (space) is the Compose v2+ plugin. `docker-compose` (hyphen) is the retired v1 Python program. Don't install it.

### `sh scripts/doctor.sh`
- **Working directory:** repository root
- **Where it runs:** host. It starts one `hello-world` container.
- **Exit status:** 0 if everything required passes, 1 otherwise. This makes it usable in other scripts.

## Code

### `scripts/doctor.sh`

| Lines | What it does | Why it's written this way |
|---|---|---|
| `#!/bin/sh` | Runs with the POSIX shell | Works on macOS, Linux and WSL without bash-specific features |
| `ok` / `bad` / `note` functions | Print a coloured status line; `bad` also prints a fix and sets `fail=1` | Every failure tells you what to do next |
| `version_ge` | Compares dotted versions with `sort -t. -k1,1n …` | Plain string comparison gets `2.9 > 2.40` wrong |
| Git block | Version ≥ 2.40, then `user.name` and `user.email` | Commits fail later without an identity |
| uv / Python block | `uv python find 3.14` | Checks what uv can actually use, not whatever `python3` happens to be |
| Docker block | Checks the client, **then** `docker version --format '{{.Server.Version}}'` for the daemon, then runs `hello-world` | Separates "installed" from "running" from "can run containers" |
| `docker info --format '{{.MemTotal}}'` | Reads the memory available to Docker | Under 4 GB, later modules run out of memory |
| WSL block | Detects WSL via `/proc/version` and warns about `/mnt/...` paths | Bind mounts across the Windows boundary are very slow |
| `exit "$fail"` | Non-zero exit if anything required failed | Scripts and CI can depend on it |

## Tradeoffs and alternatives
- **Docker Desktop vs. alternatives** (OrbStack, Colima, Podman): all can work, but the course is recorded and verified with Docker Desktop. With an alternative, paths and memory settings differ.
- **`docker` group vs. `sudo` vs. rootless Docker (Linux):** the `docker` group is convenient and root-equivalent. Rootless Docker is safer but changes networking and port details. The course assumes either the group or sudo.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `uv: command not found` right after installing | The shell hasn't reloaded `PATH` | Open a new terminal |
| `permission denied while trying to connect to the Docker daemon socket` (Linux) | Your user can't access `/var/run/docker.sock` | Use `sudo`, or join the `docker` group and log out and back in |
| Very slow container startup on Windows | Code under `/mnt/c` | Move the clone under `~` in WSL |
| `docker: 'compose' is not a docker command` | The Compose plugin isn't installed | Install `docker-compose-plugin` (Linux) or update Docker Desktop |
