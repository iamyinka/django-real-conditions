# Storyboard — M01.03 Images, containers, and layers: the Dockerfile

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Slide: "my machine" vs. "server" with mismatched versions; then one box labeled "image" | "OS files + Python + deps + code = one artifact" | slide | 35 |
| 2 | Diagram: one image (stacked read-only layers) → three containers, each with a thin writable layer; one container deleted, its layer vanishes | "image = template · container = running instance + writable layer" | diagram `m1-image-container` | 60 |
| 3 | Editor: Dockerfile lines 1–8 | `# syntax=docker/dockerfile:1`, `FROM python:3.14.10-slim-trixie` | `Dockerfile` at `lesson/M01.03-end` | 50 |
| 4 | Editor | `COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/` | same | 30 |
| 5 | Editor | `ENV` block, each variable highlighted in turn | same | 65 |
| 6 | Editor | `WORKDIR /app`, `COPY . .`, `RUN uv sync --locked`, `EXPOSE 8000`, `CMD [...]` | same | 75 |
| 7 | Terminal: `docker history telecom` | `51MB  COPY . .` and `61.8MB  RUN … uv sync --locked` highlighted | live | 50 |
| 8 | Diagram: terminal (host) → context tarball → daemon in Linux VM → image; then terminal `docker build -t telecom .` | "The builder only sees the context" | diagram `m1-build-context`; live | 65 |
| 9 | Terminal, then browser | `docker run --rm -p 127.0.0.1:8001:8000 -e DJANGO_SECRET_KEY=dev-only telecom`; `docker run --rm telecom python -c "…"` → `3.14.10 6.1.3`; browser `localhost:8001` welcome page | live | 80 |
| 10 | Terminal + diagram | `… telecom python manage.py runserver 127.0.0.1:8000` → `curl: (52) Empty reply from server`; diagram `m1-bind-addresses`: host 127.0.0.1:8001 → container eth0:8000 (nothing listening) vs. lo | live; diagram | 75 |
| 11 | Terminal | `docker run --rm telecom sh -c 'ls -a /app; du -sh /app/.venv; find /app/.venv -type f \| wc -l'` → `49M`, `4293`; rebuild after editing `config/urls.py` → `RUN uv sync --locked … Installed 9 packages` | live | 55 |

## Recording instructions
- Start at `lesson/M01.03-start` with the host `.venv` present (from `uv sync` in M1.2). That's what makes scene 11's problem real.
- **Port 8001 must be free:** stop any running Compose stack first (`docker compose down` in `projects/telecom`). On 2026-11-08 a leftover stack caused `Bind for 127.0.0.1:8001 failed: port is already allocated`. Keep that error in mind for M1.5.
- Numbers verified 2026-11-08 on Docker 29.3.1 (arm64): image 385 MB; `COPY . .` layer 51 MB; `/app/.venv` 49 MB, 4,293 files; rebuild after a one-line change reinstalls 9 packages (4.7 s); runserver bound to 127.0.0.1 inside → `Empty reply from server`.
