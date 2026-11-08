# Storyboard — M00.02 Your toolchain, verified

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Slide | "Installed ≠ working" | slide | 25 |
| 2 | Slide: four tool cards + editor | Git · uv · Docker · Compose · (editor) | slide | 40 |
| 3 | Terminal | `git --version` → `git version 2.50.1`; then `git config --global user.name` / `user.email` (email blurred except the `noreply` domain) | live terminal | 55 |
| 4 | Browser still of the uv install page, then terminal | `uv --version` → `uv 0.13.7`; `uv python install 3.14`; `uv python find 3.14`. Caption: "Apps use the Python **in the image**" | docs.astral.sh/uv; live terminal | 85 |
| 5 | Terminal + diagram | `docker version` with **Client** and **Server** blocks boxed; diagram `m0-docker-halves`: CLI → daemon in a Linux VM (Docker Desktop) | live terminal; diagram | 70 |
| 6 | Terminal (Docker Desktop quit first) | Error line highlighted: `Cannot connect to the Docker daemon at unix:///…/docker.sock. Is the docker daemon running?`; then Docker Desktop started, `docker version` again with both blocks | live terminal | 60 |
| 7 | Terminal | `docker run --rm hello-world` → "Hello from Docker!" | live terminal | 45 |
| 8 | Terminal | `docker compose version` → `Docker Compose version v5.1.1`; caption "~~docker-compose~~ (retired)" | live terminal | 35 |
| 9 | Slide: three platform columns | Linux: docker group = root-equivalent · WSL2: code under `~`, not `/mnt/c` · All: ≥ 4 GB (8 GB later) | slide | 60 |
| 10 | Terminal | `sh scripts/doctor.sh`, all `ok`; then the same with `DOCKER_HOST=unix:///nonexistent.sock` to show a `FAIL` with its fix | live terminal | 70 |
| 11 | Slide | "Next: one repository, five apps" | slide | 10 |

## Recording instructions
- macOS host, Docker Desktop running at the start. Terminal 120×32, 18 px font.
- Scene 6: quit Docker Desktop from the menu bar **before** recording the scene. Wait for it to stop fully. Restart it on camera and cut the wait.
- Scene 10's failure demo uses `DOCKER_HOST` to point at a socket that doesn't exist, so Docker Desktop doesn't need to be quit again. Say on screen: "Simulated failure: DOCKER_HOST points nowhere". **Label: Simulated** (for that clip only).
- Blur the git email except the `users.noreply.github.com` domain.
