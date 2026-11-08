# Storyboard — M01.08 Health checks, readiness, and startup order

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Timeline diagram: db "started" → (gap: initializing) → "accepting connections"; web starts inside the gap | "started ≠ ready" | diagram `m1-started-vs-ready` | 45 |
| 2 | Slide: two columns | **Liveness:** alive? → restart · **Readiness:** can work? → stop traffic | slide | 40 |
| 3 | Editor: `core/views.py` | `healthz`; `readyz` with `cursor.execute("SELECT 1")`, `except DatabaseError`, `status=503`; decorators | `core/views.py` at `-end` | 80 |
| 4 | Editor: `base.py` | `"OPTIONS": {"connect_timeout": 5}` | `config/settings/base.py` | 25 |
| 5 | Editor: `core/management/commands/wait_for_db.py` | `deadline = time.monotonic() + timeout`; `ensure_connection()`; `raise CommandError(…)` | file at `-end` | 60 |
| 6 | Editor: `compose.yaml` diff | db `healthcheck` (`pg_isready -h 127.0.0.1 …`); web `depends_on: db: condition: service_healthy`; web `healthcheck` (urllib); `start_period`, `start_interval`; `command: sh -c "python manage.py wait_for_db --timeout 30 && exec …"` | `git diff lesson/M01.08-start lesson/M01.08-end -- compose.yaml` | 95 |
| 7 | Terminal | `docker compose down -v && docker compose up -d --build` → `Container telecom-db-1 Waiting` → `Healthy` → `Container telecom-web-1 Starting`; `docker compose logs web` → `Database available (attempt 1).`; `docker compose ps` → both `(healthy)` | live | 55 |
| 8 | Terminal | `docker compose stop db`; `curl -s -w ' %{http_code}\n' localhost:8001/healthz` → `{"status": "ok"} 200`; `…/readyz` → `{"status": "unavailable", …} 503`; logs → `failed to resolve host 'db'`; `docker compose exec web python manage.py wait_for_db --timeout 3` → `CommandError: Database still unavailable after 3 attempts (3s)`, exit 1; `docker compose start db` → `Database available (attempt 1).`, readyz 200 | live | 90 |
| 9 | Terminal: output of the probe script | `poll 4: socket=up tcp=down` highlighted; db logs `PostgreSQL init process complete; ready for start up.` | probe script (recording instructions) | 60 |
| 10 | Editor: `tests/test_health.py`, `tests/test_wait_for_db.py`; terminal `docker compose exec web pytest -q` → `16 passed` | Test names highlighted | files at `-end`; live | 55 |
| 11 | Slide | "Next: non-root and secrets" | slide | 10 |

## Recording instructions
- Scene 9 uses this script (run from any directory). It needs no project files:
  ```bash
  docker rm -f pgprobe 2>/dev/null
  docker run -d --name pgprobe -e POSTGRES_PASSWORD=x -e POSTGRES_DB=probe postgres:18.6-trixie >/dev/null
  prev=""; n=0
  for i in $(seq 1 150); do
    s=$(docker exec pgprobe pg_isready -q -U postgres -d probe && echo up || echo down)
    t=$(docker exec pgprobe pg_isready -q -h 127.0.0.1 -U postgres -d probe && echo up || echo down)
    cur="socket=$s tcp=$t"; [ "$cur" != "$prev" ] && echo "poll $i: $cur" && prev="$cur"
    [ "$s" = up ] && [ "$t" = up ] && n=$((n+1)) && [ "$n" -ge 5 ] && break
  done
  docker rm -f pgprobe >/dev/null
  ```
  Verified 2026-11-07 output: `poll 1: socket=down tcp=down`, `poll 4: socket=up tcp=down`, `poll 5: socket=down tcp=down`, `poll 6: socket=up tcp=up`. Timing varies by machine; if the window doesn't appear in a take, run it again and say so on screen rather than faking it.
- The `wait_for_db` failure took 3 attempts in real time (each connection attempt takes time), versus 4 in the fake-clock unit test. Both are correct for their clocks.
