# Notes — M01.08 Health checks, readiness, and startup order

## Code

### `core/views.py`

| Line(s) | What it does | When it runs | Why |
|---|---|---|---|
| `@never_cache` | Adds `Cache-Control: max-age=0, no-cache, no-store, must-revalidate, private` | Each response | A cached "ok" is a lie |
| `@require_GET` | Other methods → 405 | Each request | Probes are read-only |
| `healthz`: `return JsonResponse({"status": "ok"})` | Liveness: no database, no cache, no other service | Request | A DB outage mustn't make the process look dead |
| `readyz`: `with connection.cursor() as cursor: cursor.execute("SELECT 1")` | Round-trip to Postgres | Request | Proves the database answers queries, not just that a socket opens |
| `except DatabaseError:` | Catches connection and query failures (`OperationalError` is a subclass) | On failure | Narrow enough not to hide programming errors |
| `logger.exception(...)` | Logs the message **and traceback** | On failure | Operators get details |
| `JsonResponse({...}, status=503)` | `503 Service Unavailable` | On failure | Standard "not ready, try later" signal for load balancers |

### `core/urls.py` and `config/urls.py`
`path("healthz", …)` and `path("readyz", …)`, without trailing slashes (conventional for probes), included at the root with `path("", include("core.urls"))`. `core` is added to `INSTALLED_APPS` so Django discovers its management command.

### `config/settings/base.py`
`"OPTIONS": {"connect_timeout": 5}` is passed to libpq/psycopg as the connection timeout in seconds.

### `core/management/commands/wait_for_db.py`

| Line(s) | What it does | Why |
|---|---|---|
| File location `core/management/commands/` | Django discovers `wait_for_db` as a command | Each folder needs an `__init__.py` |
| `class Command(BaseCommand)` | Standard management command | Gives argument parsing, `stdout`/`stderr`, styling |
| `add_arguments`: `--timeout` (30), `--interval` (1) | Configurable bounds | Different environments need different patience |
| `deadline = time.monotonic() + timeout` | Monotonic clock | Unaffected by NTP or manual clock changes |
| `connection.ensure_connection()` | Opens a connection if there isn't one | Raises `OperationalError` if it can't |
| `if time.monotonic() + interval > deadline: raise CommandError(...) from exc` | Gives up when the next try would pass the deadline | `CommandError` → message on stderr, exit status 1 |
| `self.stderr.write(...)`, `time.sleep(interval)` | Report, then wait | Visible progress in logs |

### `compose.yaml` (changes)

| Key | Meaning | Why |
|---|---|---|
| `db.healthcheck.test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]` | Run in the db container's shell | `-h 127.0.0.1` forces TCP. `$$` escapes Compose interpolation, so the container's shell expands the variables. |
| `interval: 5s`, `timeout: 3s`, `retries: 5` | Probe every 5 s; a probe taking > 3 s fails; 5 failures in a row = unhealthy | |
| `start_period: 30s`, `start_interval: 1s` | Failures during the first 30 s don't count; probe every 1 s meanwhile | Fast "healthy" without false "unhealthy" while booting |
| `web.depends_on: db: condition: service_healthy` | Start web only after db is healthy | Closes the started/ready gap at `up` |
| `web.healthcheck.test: [CMD, python, -c, "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"]` | `urlopen` raises on errors and 4xx/5xx → non-zero exit → unhealthy | No curl in slim images. Liveness, not readiness. |
| `web.command: sh -c "python manage.py wait_for_db --timeout 30 && exec python manage.py runserver 0.0.0.0:8000"` | Wait, then serve | `&&`: only serve if waiting succeeded. `exec` replaces the shell with Python, so stop signals reach Django directly. |

### Tests (`tests/test_health.py`, `tests/test_wait_for_db.py`)

| Test | Proves |
|---|---|
| `test_healthz_is_ok_without_touching_the_database` | No `django_db` mark → pytest-django **fails** the test on any DB access |
| `test_healthz_rejects_post` | 405 |
| `test_readyz_is_ok_when_database_answers` | Real query against Postgres |
| `test_readyz_is_503_and_hides_details_when_database_fails` | Patches `core.views.connection` so the cursor raises `OperationalError("password authentication failed")`; asserts 503 and that `"password"` isn't in the body |
| `test_returns_once_database_comes_up` | `ensure_connection` fails twice, then succeeds → 3 calls, 2 sleeps |
| `test_gives_up_after_the_deadline` | Fake `monotonic` + `sleep` advance a fake clock: tries at t=0,1,2,3 → `CommandError … after 4 attempts` |

## Commands

| Command | Expected |
|---|---|
| `docker compose ps` | `Up … (healthy)` for both |
| `curl -s -w ' %{http_code}\n' localhost:8001/healthz` | `{"status": "ok"} 200` |
| `curl … /readyz` (db up / stopped) | `200` / `{"status": "unavailable", "checks": {"database": "error"}} 503` |
| `docker compose stop db` / `start db` | Stops/starts db without removing it |
| `docker compose exec web python manage.py wait_for_db --timeout 3` (db stopped) | `Database unavailable (attempt 1), retrying in 1s` … `CommandError: Database still unavailable after 3 attempts (3s): failed to resolve host 'db': [Errno -2] Name or service not known`, exit 1 |
| `docker inspect -f '{{.State.Health.Status}}' telecom-web-1` | `healthy` / `starting` / `unhealthy` |

## Tradeoffs and alternatives
- **Readiness in the container health check:** tempting, but it cascades database problems into "web unhealthy". In orchestrators (Kubernetes, load balancers), wire `/readyz` to traffic decisions instead; Module 7.
- **`depends_on` only acts at `up`.** It doesn't restart web if db dies later. `wait_for_db` covers `run --no-deps` and platforms without Compose.
- **Docker doesn't restart unhealthy containers** by itself (Swarm and Kubernetes do). Health status is information until something acts on it.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| web stuck in `Created`, never starts | db never becomes healthy | `docker compose logs db`; `docker inspect telecom-db-1 --format '{{json .State.Health}}'` |
| db `unhealthy` with `pg_isready` "no response" | Wrong user or db name in the check, or `$` not escaped as `$$` | Check the `test` line |
| web `unhealthy` but the page loads in the browser | `ALLOWED_HOSTS` rejects `127.0.0.1` | Include it in `DJANGO_ALLOWED_HOSTS` |
| `/readyz` slow when the DB host is unreachable | No `connect_timeout` | Set it (5 s here) |
