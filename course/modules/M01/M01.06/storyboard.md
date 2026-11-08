# Storyboard — M01.06 Volumes: bind mounts vs. named volumes

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Terminal at `-start` | `docker compose exec db psql -U telecom -d telecom -c "create table notes(t text); insert into notes values ('survive?')"` → `select * from notes` (1 row) → `docker compose down` → `up -d` → `select …` → `ERROR: relation "notes" does not exist` | live | 65 |
| 2 | Diagram + terminal | Container (writable layer) + anonymous volume `a1b2…`; after down/up a second anonymous volume appears; `docker volume ls` shows two hex names. `docker image inspect postgres:18.6-trixie -f '{{json .Config.Volumes}}'` → `{"/var/lib/postgresql":{}}` | diagram `m1-anonymous-volume`; live | 80 |
| 3 | Editor: `compose.yaml` diff | `volumes: - pgdata:/var/lib/postgresql` under db; top-level `volumes: pgdata:` | `git diff lesson/M01.06-start lesson/M01.06-end -- compose.yaml` | 45 |
| 4 | Terminal | `docker run --name pg18old -e POSTGRES_PASSWORD=x -v pg18old:/var/lib/postgresql/data postgres:18.6-trixie` → `Error: in 18+, these Docker images are configured to store database data in a format which is compatible with "pg_ctlcluster"…` → exit code 1; `PGDATA=/var/lib/postgresql/18/docker` | live | 70 |
| 5 | Terminal | `up -d` → create + insert → `down` → `up -d` → `select` → 1 row | live | 40 |
| 6 | Terminal | `docker compose down -v` → `Volume telecom_pgdata Removed` → `up -d` → `relation "notes" does not exist` | live | 50 |
| 7 | Editor + diagram | `volumes: - .:/app` under web; diagram: host folder ↔ `/app` (same files) | `compose.yaml`; diagram `m1-bind-mount` | 50 |
| 8 | Diagram | `/app` (bind mount, host code) and `/opt/venv` (image) side by side | diagram | 35 |
| 9 | Split: editor saves `config/urls.py`; terminal `docker compose logs -f web` | `… changed, reloading.` / `Watching for file changes with StatReloader` | live | 45 |
| 10 | Slide: three columns | Writable layer · Named volume · Bind mount | slide | 40 |

## Recording instructions
- Start with the M1.5 stack running at `lesson/M01.06-start` and freshly migrated.
- Scene 2: clean up orphaned volumes off camera first (`docker volume prune` only after checking `docker volume ls`: it deletes **every** unused volume on the machine).
- Scene 4: remove the demo container and volume afterwards: `docker rm -f pg18old; docker volume rm pg18old`.
- Verified 2026-11-08: anonymous volume → data lost after down/up; named → kept after down/up, removed by `down -v`; PG 18.6 + `/var/lib/postgresql/data` → exit 1 with the message above; bind-mount reload works.
