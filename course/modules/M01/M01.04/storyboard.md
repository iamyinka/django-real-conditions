# Storyboard — M01.04 Build context, .dockerignore, locking, and caching

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Editor: M1.3 Dockerfile | `COPY . .` highlighted in red | `Dockerfile` at `-start` | 25 |
| 2 | Terminal: `docker build --progress=plain -t telecom .` | `transferring context: 663.88kB` highlighted | live | 55 |
| 3 | Terminal, **Simulated** badge | `printf 'POSTGRES_PASSWORD=demo-fake-password\n' > .env` → build → `docker run --rm telecom cat /app/.env` → the password | live | 60 |
| 4 | Editor `.dockerignore`, then terminal | Sections highlighted in turn; rebuild → `transferring context: 1.37kB`; `docker run --rm telecom cat /app/.env` → `No such file or directory` | `.dockerignore` at `-end`; live | 85 |
| 5 | Diagram: layer stack with cache hits (green) until the first change (red), everything below red; then terminal rebuild at `-start` after editing `config/urls.py` | `#11 [5/5] RUN uv sync --locked … Installed 9 packages … DONE 4.7s` | diagram `m1-cache-chain`; live | 70 |
| 6 | Editor: diff `-start` → `-end` Dockerfile | `COPY pyproject.toml uv.lock ./` moved above; `COPY . .` moved last | `git diff lesson/M01.04-start lesson/M01.04-end -- Dockerfile` | 45 |
| 7 | Editor | `RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-install-project`; `UV_COMPILE_BYTECODE=1`, `UV_LINK_MODE=copy` | `Dockerfile` at `-end` | 80 |
| 8 | Terminal | Second build after a code edit: `[5/6] RUN --mount=… uv sync … CACHED`, `[6/6] COPY . . DONE 0.0s`; `docker images` → `341MB` | live | 50 |
| 9 | Editor split: `pyproject.toml` / `uv.lock` (one package entry with `hash = "sha256:…"`) | "want" vs. "got" | repo | 45 |
| 10 | Slide | "Next: Compose with Postgres" | slide | 10 |

## Recording instructions
- Scenes 2–5 at `lesson/M01.04-start`; scenes 6–9 at `lesson/M01.04-end`.
- For cache demos, the code edit must be **unique** each time (for example `echo "# $(date +%s)" >> config/urls.py`). Repeating an identical edit gives a cache hit even at `-start`, which would make the "before" demo lie. Restore with `git checkout -- config/urls.py`.
- Delete the demo `.env` after scene 4 (`rm .env`). M1.5 creates the real one from `.env.example`.
- Numbers verified 2026-11-08: context 663.88 kB → 1.37 kB; `-start` rebuild installs 9 packages in 4.7 s; `-end` rebuild has `uv sync` CACHED; image 385 MB → 341 MB.
