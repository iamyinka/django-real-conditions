# Notes — M01.07 Management commands inside containers

The everyday command table lives in [`projects/telecom/README.md`](../../../../projects/telecom/README.md). These notes break the commands down.

## Commands

### `docker compose exec web python manage.py migrate`
- **Working directory:** `projects/telecom/` (where `compose.yaml` is)
- **Prerequisites:** the stack is up (`docker compose ps` shows web running)

| Part | Runs where | Meaning |
|---|---|---|
| `docker compose` | Host | Reads `compose.yaml`, finds services |
| `exec` | Host → Docker | Run a process in an **already running** container |
| `web` | | The target service |
| `python manage.py` | Web container | The venv's Python (`/opt/venv/bin` is first on `PATH`) runs Django's CLI. `DJANGO_SETTINGS_MODULE` defaults to `config.settings.dev`. |
| `migrate` | Web container → db | Applies unapplied migrations over the network to Postgres; records each one in `django_migrations` |

- **Expected output:** `Applying contenttypes.0001_initial... OK` … (18 on a fresh database), or `No migrations to apply.`
- **Idempotent:** safe to run repeatedly.

### `docker compose exec web python manage.py showmigrations auth`
`[X]` = applied, `[ ]` = pending. Omit `auth` to list every app.

### `docker compose restart web`
Stops and starts the same container. **No** migrations, **no** rebuild, **no** new environment from a changed `compose.yaml` (that needs `up -d`, which recreates it).

### `docker compose exec web python manage.py shell -c "…"`
- `shell`: Python with Django set up.
- `-c "code"`: run the code and exit. Good for scripts and quick checks.

### `docker compose exec -e DJANGO_SUPERUSER_PASSWORD=… web python manage.py createsuperuser --noinput --username admin --email admin@example.test`

| Part | Meaning |
|---|---|
| `-e NAME=value` | Set an environment variable for this exec'd process only |
| `DJANGO_SUPERUSER_PASSWORD` | Read by `createsuperuser` when `--noinput` is used |
| `--noinput` | No prompts; fail if something required is missing |
| `--username`, `--email` | Field values |

**Security:** a password typed on the command line ends up in your shell history and is visible in the process list. Fine for a throwaway dev admin; never for real credentials.

### `docker compose run --rm --no-deps web hostname`

| Part | Meaning |
|---|---|
| `run` | Create a **new** container from the `web` service definition and run the command |
| `--rm` | Remove it afterwards |
| `--no-deps` | Don't start the services in `depends_on` |
| `hostname` | Prints the container's hostname (its short ID by default) |

### `docker compose exec web pytest -q`
Runs the suite inside web, where the tests reach Postgres as `db`. `-q` = quiet output. Expected at this checkpoint: `10 passed`.

### `docker compose exec web python manage.py makemigrations --check --dry-run`
- `--check`: exit non-zero if model changes lack a migration.
- `--dry-run`: don't write files.
- Expected: `No changes detected`. CI runs this in Module 7.

### `docker compose logs -f web`
`-f` follows new output. Add `--tail 50` to start with the last 50 lines.

## exec vs. run

| | `exec` | `run` |
|---|---|---|
| Container | The running one | A new one |
| Needs the service up | Yes | No |
| Shares state (files written, processes) | Yes | No |
| Ports published | (already) | Not by default (`--service-ports` to publish) |
| Typical use | migrate, shell, tests | One-off jobs, debugging a service that won't start |

## Tradeoffs and alternatives
- **Running migrations automatically at container start** (in an entrypoint) is common in small setups. It gets risky with several replicas starting at once, and it hides a deploy step. The course keeps `migrate` explicit; Module 7 makes it a deploy step.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `service "web" is not running` | `exec` needs a running container | `docker compose up -d`, or use `run --rm` |
| `no configuration file provided: not found` | Wrong directory | `cd projects/telecom` |
| `relation "auth_user" does not exist` | Migrations not applied | `docker compose exec web python manage.py migrate` |
| `CommandError: You must use --username with --noinput.` | Missing a required field | Add `--username` and `--email` |
