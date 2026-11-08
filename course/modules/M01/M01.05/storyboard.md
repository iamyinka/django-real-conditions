# Storyboard — M01.05 Compose: Django and PostgreSQL

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Slide | "Develop on the database you deploy on" | slide | 35 |
| 2 | Diagram: `compose.yaml` → two boxes, web and db, on one network | `services:` · `web` · `db` | diagram `m1-compose-two-services` | 30 |
| 3 | Terminal, then editor diff of `base.py` | `uv add "psycopg[binary]==3.3.8"`; `DATABASES` with `env("POSTGRES_DB")` … `"HOST": env("DB_HOST")` | `git diff lesson/M01.05-start lesson/M01.05-end -- config/settings/base.py` | 55 |
| 4 | Editor `.env.example`; terminal `cp .env.example .env` | Comment "reads POSTGRES_* only the FIRST time…" highlighted | `.env.example` | 50 |
| 5 | Editor `compose.yaml` at `-end`, block by block | `name:`, `build: .`, `env_file`, `ports`, `depends_on` + comment, `image: postgres:18.6-trixie`, `${POSTGRES_…}`, no `ports:` under db | `compose.yaml` | 100 |
| 6 | Terminal, then browser | `docker compose up -d --build` → `Network telecom_default Created`; `docker compose ps`; `docker compose exec web python manage.py migrate` → `Applying … OK` ×18; browser `localhost:8001` | live | 75 |
| 7 | Terminal + diagram | `docker compose exec web python -c "import socket; print(socket.gethostbyname('db'))"` → `172.22.0.2`; same for `localhost` → `127.0.0.1`; diagram with an embedded DNS box | live; diagram `m1-compose-dns` | 50 |
| 8 | Terminal | `docker compose exec -e DB_HOST=localhost web python manage.py migrate` → `connection to server at "127.0.0.1", port 5432 failed: Connection refused` / `Is the server running on that host and accepting TCP/IP connections?` | live | 60 |
| 9 | Diagram: host with Postgres.app on 5432; Docker network with db:5432 (no door); a GUI tool connecting to the host one | "No error. Wrong database." | diagram `m1-two-postgres`; `lsof -nP -iTCP:5432 -sTCP:LISTEN` → `postgres 127.0.0.1:5432` | 70 |
| 10 | Terminal | Second stack already holding 8001 → `Bind for 127.0.0.1:8001 failed: port is already allocated`; `docker ps --format '{{.Names}} {{.Ports}}'` | live | 45 |
| 11 | Slide | "Next: where does the data live?" | slide | 10 |

## Recording instructions
- Start from `lesson/M01.05-start` with **no** telecom containers running (`docker compose down -v` first).
- Scene 9: the Postgres.app part is real on the recording machine. On a machine without it, show the diagram only and say so.
- Scene 10: reproduce with `docker run -d --rm --name squatter -p 127.0.0.1:8001:80 nginx:alpine` **before** `docker compose up`, then stop it with `docker stop squatter`.
- Outputs verified 2026-11-08: 18 migrations applied; `db -> 172.22.0.2` (the address varies); the localhost error text above; Postgres.app on `127.0.0.1:5432` and `[::1]:5432`; the port-conflict message.
