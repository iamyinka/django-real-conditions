# Telecom operations & field service

This is Project 1 of *Django Under Real Conditions*. Right now it's a runnable skeleton: Django 6.1 and PostgreSQL 18 in Docker Compose. Business features arrive in Module 2 onward.

## Prerequisites

- Docker with Compose v2 (`docker compose version`)
- Run every command below from **this directory**: `projects/telecom/`

## Start

```bash
cp .env.example .env          # local, git-ignored config with throwaway dev values
docker compose up -d --build  # build the web image, start web + db in the background
docker compose exec web python manage.py migrate
```

Then open http://localhost:8001/.

## Everyday commands: what runs where

| Command | Where it runs | What it does |
|---|---|---|
| `docker compose up -d --build` | Host → Docker | Builds the image if needed, then creates and starts the containers. `-d` returns your terminal. |
| `docker compose ps` | Host | Shows the containers' state, health, and published ports. |
| `docker compose logs -f web` | Host | Follows the web container's output. Ctrl+C stops following, not the container. |
| `docker compose exec web python manage.py migrate` | Inside the **running** `web` container | Applies migrations to the database that `DB_HOST` points to (`db`). |
| `docker compose exec web python manage.py showmigrations` | Inside `web` | `[X]` means applied and `[ ]` means pending. |
| `docker compose exec web python manage.py createsuperuser` | Inside `web` | Interactive admin user creation. |
| `docker compose exec web python manage.py shell` | Inside `web` | A Python shell with Django configured. |
| `docker compose exec web pytest` | Inside `web` | Runs the tests against the Postgres container. |
| `docker compose run --rm web <cmd>` | In a **new, temporary** `web` container | Runs a one-off command even when `web` isn't running. `--rm` deletes the container afterwards. |
| `docker compose exec db psql -U telecom -d telecom` | Inside `db` | A SQL prompt on the project's database. |
| `docker compose down` | Host | Stops and removes the containers and network. **The `pgdata` volume is kept.** |
| `docker compose down -v` | Host | The same, **plus it deletes the database volume**, and with it all the data. |

### Restarting doesn't migrate

`docker compose restart web` restarts the same code against the same database. It never applies migrations. We verified this: after a restart on a fresh database, `showmigrations` still shows `[ ]`. Migrations run only when you run `migrate`. In production, that's an explicit deploy step (Module 7).

### `exec` vs `run`

`exec` enters the container that's already running, so it shares that container's state. `run` creates a new container from the same service definition: it has a different hostname and its own temporary filesystem. Use `run --rm` for one-off tasks when the service isn't up.

## Health checks

| URL / command | Answers | DB down |
|---|---|---|
| `GET /healthz` | Is the process serving requests? (liveness) | Still `200`. Restarting web wouldn't fix the DB. |
| `GET /readyz` | Can this instance do useful work? (readiness: `SELECT 1`) | `503 {"status": "unavailable"}`. Details go to the logs, not the response. |
| `python manage.py wait_for_db --timeout 30` | Blocks until the DB accepts connections, then exits 0 | Exits 1 with `CommandError` after the deadline |

`docker compose ps` shows each container's health. `web` doesn't start until `db` reports `healthy` (`depends_on: condition: service_healthy`).

## Configuration

Settings are read from environment variables (see `.env.example`). The settings modules are:

- `config.settings.dev`: the default for `manage.py`. Debug is on and only localhost is allowed.
- `config.settings.test`: used by pytest, configured in `pyproject.toml`.

A missing required variable stops startup with `ImproperlyConfigured: Set the <NAME> environment variable.`

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `connection to server at "127.0.0.1", port 5432 failed: Connection refused` | `DB_HOST=localhost`. Inside a container, `localhost` is that container itself. | Set `DB_HOST=db`, the Compose service name. |
| `relation "…" does not exist` after `down` + `up` | The data was in a volume that got removed (`down -v`) or replaced. | Run `migrate` again. Keep data in the named `pgdata` volume. |
| A host tool "connects to the database" but sees different data | Something else is listening on host port 5432, such as Postgres.app. This project's database isn't published to the host. | Use `docker compose exec db psql …` to reach the container's database. |
| `ImproperlyConfigured: Set the DJANGO_SECRET_KEY…` | No `.env` file, or a missing variable. | `cp .env.example .env` |
