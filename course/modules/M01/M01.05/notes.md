# Notes — M01.05 Compose: Django and PostgreSQL

## Code

### `config/settings/base.py`: `DATABASES`

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", "5432"),
    }
}
```

| Key | Meaning | Why |
|---|---|---|
| `ENGINE` | Django's PostgreSQL backend, which uses psycopg 3 | |
| `NAME`/`USER`/`PASSWORD` | Same variable names the Postgres image uses | One `.env` feeds both containers |
| `HOST: env("DB_HOST")` | Required. `db` in Compose. | A missing host fails at startup, not at the first query |
| `PORT` | Defaults to 5432 | The container port, not a published host port |

### `config/settings/test.py` (added lines)
Sets `POSTGRES_*` and `DB_HOST=localhost` defaults with `setdefault` **before** importing base, so tests that don't touch the database can run anywhere. Database tests run in the web container, where the real `.env` values win.

### `compose.yaml`

| Line | Meaning | Why |
|---|---|---|
| `name: telecom` | The Compose project name | Prefix for containers (`telecom-web-1`), network (`telecom_default`), volumes. Stops collisions between projects. |
| `web.build: .` | Build the image from `./Dockerfile` | Same image as M1.4 |
| `web.env_file: .env` | Load every variable from `.env` into the container | Django reads them at startup |
| `web.ports: "127.0.0.1:8001:8000"` | Publish host 127.0.0.1:8001 → container 8000 | Host-only; 8001 avoids clashing with other things on 8000 |
| `web.depends_on: [db]` | Start db before web | **Order only.** Doesn't wait for Postgres to be ready (M1.8). |
| `db.image: postgres:18.6-trixie` | Official image, exact version | Matches `course/VERSIONS.md` |
| `db.environment: POSTGRES_DB: ${POSTGRES_DB}` | `${…}` is **Compose interpolation**: Compose substitutes the value from `.env` when it reads this file | Gives Postgres only what it needs |
| *(no `db.ports`)* | Postgres isn't published | Reachable only as `db:5432` from containers on this network |

**Two ways `.env` is used:** Compose reads `.env` in the project directory automatically for `${VAR}` interpolation. Separately, `env_file: .env` injects its variables into the web container. Same file, two mechanisms.

## Commands

### `docker compose up -d --build`
- **Working directory:** `projects/telecom/`

| Part | Meaning |
|---|---|
| `docker compose` | The Compose plugin; reads `compose.yaml` from the current directory |
| `up` | Create the network, build or pull images, create and start containers |
| `-d` | Detached: return the terminal; containers keep running |
| `--build` | Rebuild images even if one exists |

- **Expected output:** `Network telecom_default Created`, `Container telecom-db-1 Started`, `Container telecom-web-1 Started`.
- **Verify:** `docker compose ps` lists both as `Up`.

### `docker compose exec web python manage.py migrate`
See M1.7 for a part-by-part breakdown. Expected: 18 lines of `Applying <app>.<migration>... OK` (contenttypes, auth, admin, sessions).

### `docker compose exec web python -c "import socket; print(socket.gethostbyname('db'))"`
Resolves the service name with Python's standard library, from inside web. Prints the db container's address on `telecom_default` (172.22.0.2 when recorded; it varies).

### `docker compose exec -e DB_HOST=localhost web python manage.py migrate`
`-e` overrides an environment variable for this one exec'd process. Expected failure:
```
psycopg.OperationalError: connection failed: connection to server at "127.0.0.1", port 5432 failed: Connection refused
	Is the server running on that host and accepting TCP/IP connections?
```

### `lsof -nP -iTCP:5432 -sTCP:LISTEN` (macOS/Linux host)
Lists processes listening on TCP 5432 **on the host**. `-n`/`-P`: don't resolve names or ports. On the recording machine, Postgres.app was listening, while the course database wasn't published at all.

## Reading "Connection refused"

| Message | Means | Typical cause here |
|---|---|---|
| `Connection refused` | The host was reached; nothing listens on that port | Wrong host (`localhost` inside a container), or the db isn't up yet |
| `could not translate host name "db"` / `failed to resolve host` | DNS failed | Not on the Compose network, or the db container is stopped (M1.8) |
| `timeout expired` | No answer at all | Firewall or wrong network; M1.8 sets `connect_timeout` |
| `password authentication failed` | Reached Postgres, wrong credentials | `.env` changed after the database was initialized (M1.6) |

## Tradeoffs and alternatives
- **Publishing db to the host** (`"127.0.0.1:5433:5432"`) is handy for GUI tools. Use a different host port, so it can't be confused with a local Postgres on 5432. The course keeps it unpublished and uses `docker compose exec db psql`.
- **`psycopg[binary]` vs. `psycopg[c]`:** binary wheels are simplest; the C build needs libpq headers and compilers.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Bind for 127.0.0.1:8001 failed: port is already allocated` | `docker ps` to find the owner; stop it, or change the host port |
| `ImproperlyConfigured: Set the POSTGRES_DB…` | `cp .env.example .env` |
| Changed `POSTGRES_PASSWORD` in `.env`, now `password authentication failed` | The database was initialized with the old one. In dev: `docker compose down -v` (deletes data) and `up` again. |
