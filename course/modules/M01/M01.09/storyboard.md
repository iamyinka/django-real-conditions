# Storyboard — M01.09 Non-root containers, permissions, and secrets in development

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Terminal at `-start` | `docker compose exec web id` → `uid=0(root) gid=0(root) groups=0(root)` | live | 25 |
| 2 | Diagram: container walls; a process inside labeled "root"; a crack in the wall | "Isolation reduces risk; it doesn't remove it" | diagram `m1-root-in-container` | 50 |
| 3 | Editor: Dockerfile diff | `ARG UID=1000`, `ARG GID=1000`, `groupadd`/`useradd` line, `USER app`; comment "code stays owned by root" | `git diff lesson/M01.09-start lesson/M01.09-end -- Dockerfile` | 70 |
| 4 | Terminal | `docker compose up -d --build`; `docker compose exec web id` → `uid=1000(app) gid=1000(app) groups=1000(app)`; `touch /x` → `Permission denied`; `touch /opt/venv/x` → `Permission denied`; `pip install six` → `[Errno 13] Permission denied`; `docker compose ps` → web `(healthy)` | live | 60 |
| 5 | Terminal replay (reconstructed), then `git diff` of `manage.py` showing `+x`, then `git checkout -- manage.py`; then the correct test | `docker compose run … sh -c 'echo x >> /app/manage.py'` (red) vs. `docker run --rm --entrypoint "" telecom-web sh -c 'echo x >> /app/manage.py'` → `cannot create /app/manage.py: Permission denied` | reconstructed from the 2026-11-07 session; live | 70 |
| 6 | Diagram: Linux host user 1001 vs. container user 1000 → file owned by 1000; then `docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)` | "Docker Desktop maps ownership; Linux doesn't" | diagram `m1-uid-mismatch` | 60 |
| 7 | Terminal | `git check-ignore -v projects/telecom/.env` → `.gitignore:2:.env`; `git ls-files \| grep -c '\.env$'` → `0`; `docker run --rm --entrypoint "" telecom-web ls -a /app` (no `.env`); `docker history --no-trunc telecom-web \| grep -ciE "dev-only\|SECRET_KEY\|PASSWORD"` → `0` | live | 55 |
| 8 | Terminal + slide | `docker compose exec web env \| grep -E 'SECRET\|PASSWORD'` (values blurred); slide "dev: .env · prod: secret store (Module 7)" | live; slide | 50 |
| 9 | Slide: checklist of Module 1 outcomes, all ticked | Django 6.1 · Postgres 18 · env config · volumes · health · non-root | slide | 30 |

## Recording instructions
- Scene 5 is a **reconstruction** of a real mistake made while preparing the course on 2026-11-07. Label it on screen: "Reconstructed: this really happened while preparing the lesson." Perform it on camera only in a disposable clone, and restore with `git checkout -- manage.py` straight away.
- Scene 8: blur the values; they're dev placeholders, but blurring models good habits.
- Verified 2026-11-07: `uid=1000(app)`; writes to `/`, `/opt/venv` and `/app/manage.py` (image only) denied; `pip install` fails with `Permission denied: '/nonexistent'`; 16 tests pass through the bind mount; `.env` absent from git, image and history.
