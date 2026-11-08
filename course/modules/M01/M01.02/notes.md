# Notes — M01.02 Starting from nothing

## Commands

### `uv init --bare --python 3.14 --name telecom`
- **Working directory:** `projects/telecom/` (empty)
- **Where it runs:** host

| Part | Meaning |
|---|---|
| `uv init` | Create a new Python project |
| `--bare` | Create only `pyproject.toml`: no `main.py`, README, or `.python-version` |
| `--python 3.14` | Sets `requires-python = ">=3.14"`. Without it, uv used `>=3.13` on the recording machine (it picks from the interpreters it finds). |
| `--name telecom` | The project name. Defaults to the directory name. |

### `uv add django==6.1.3`

| Part | Meaning |
|---|---|
| `uv add` | Add a dependency, update the lock, and install |
| `django==6.1.3` | An exact pin. `==` means this version and no other. |

- **Side effects:** edits `pyproject.toml` (`dependencies = ["django==6.1.3"]`), writes `uv.lock`, creates `.venv/`.
- Dev-only tools go in a separate group: `uv add --dev pytest==9.2.0 pytest-django==4.14.0`.
- **Commit:** `pyproject.toml` and `uv.lock`. **Never commit:** `.venv/`.

### `uv run django-admin startproject config .`

| Part | Meaning |
|---|---|
| `uv run` | Run a command in the project's environment, syncing it first if needed. No `source .venv/bin/activate` required. |
| `django-admin` | Django's global command-line tool |
| `startproject config` | Create a project whose settings package is named `config` |
| `.` | The destination directory. Without it, Django creates `config/config/…`, one level too deep. |

### `uv run python manage.py check`
- Runs Django's system checks (configuration, models, URLs) without starting a server.
- **Expected output:** `System check identified no issues (0 silenced).`
- **If `DJANGO_SECRET_KEY` is unset:** `django.core.exceptions.ImproperlyConfigured: Set the DJANGO_SECRET_KEY environment variable.`

### `DJANGO_SECRET_KEY=dev-only uv run python manage.py runserver`
- `NAME=value command` sets an environment variable **for that one command** only (a shell feature).
- `runserver` starts Django's development server on `127.0.0.1:8000`, with auto-reload. It isn't for production (Module 7 uses Gunicorn).

### `uv run pytest`
- **Expected output:** `10 passed`.
- pytest-django reads `DJANGO_SETTINGS_MODULE = "config.settings.test"` from `[tool.pytest.ini_options]` in `pyproject.toml`.

## Code

### `manage.py`

| Line(s) | What it does | When it runs |
|---|---|---|
| `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")` | Chooses the settings module unless the environment already chose one | Every management command |
| `from django.core.management import execute_from_command_line` | Imports Django's dispatcher. The `try/except ImportError` gives a friendlier message when Django isn't installed. | Every command |
| `execute_from_command_line(sys.argv)` | Loads settings, sets up apps, finds the subcommand (`runserver`, `migrate`, …) and runs it | Every command |

### `config/env.py`

```python
_REQUIRED = object()


def env(name, default=_REQUIRED):
    value = os.environ.get(name, "")
    if value == "":
        if default is _REQUIRED:
            raise ImproperlyConfigured(f"Set the {name} environment variable.")
        return default
    return value
```

| Line(s) | What it does | Why it's written this way |
|---|---|---|
| `_REQUIRED = object()` | A unique sentinel object | Lets `default=None` be a legitimate default, distinct from "no default given" |
| `os.environ.get(name, "")` | Reads the variable; missing becomes `""` | Treats missing and empty the same: `FOO=` in an env file is almost always a mistake |
| `raise ImproperlyConfigured(…)` | Stops startup with the variable's name | Django's standard exception for configuration errors; the message says exactly what to fix |
| `env_bool`: `_TRUE = {"1","true","yes","on"}`, `_FALSE = {…}` | Accepts common spellings, case-insensitive | Anything else, like `ture`, **raises** rather than meaning `False` |
| `env_list`: `[item.strip() for item in value.split(",") if item.strip()]` | Splits on commas, trims spaces, drops blanks | `"a, b,,c "` → `["a","b","c"]` |

**When it runs:** at import time of the settings modules, which is when any management command or server starts.

### `config/settings/base.py` (key lines)

| Line | Meaning |
|---|---|
| `BASE_DIR = Path(__file__).resolve().parent.parent.parent` | `projects/telecom/`. Three levels up, because settings moved one folder deeper. |
| `SECRET_KEY = env("DJANGO_SECRET_KEY")` | Required, with no default. The generated key was deleted. |
| `DEBUG = env_bool("DJANGO_DEBUG", False)` | Secure by default: environments must opt in |
| `ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", [])` | Which `Host` headers Django answers. Empty plus `DEBUG=False` rejects every request. |
| `DATABASES` → SQLite at this checkpoint | Replaced by PostgreSQL in M1.5 |

### `config/settings/dev.py` and `test.py`

| File | Line | Meaning |
|---|---|---|
| `dev.py` | `from .base import *` | Start from everything in base (the one place a star import is deliberate) |
| `dev.py` | `DEBUG = env_bool("DJANGO_DEBUG", True)` | Debug on by default **for development only** |
| `dev.py` | `ALLOWED_HOSTS = env_list(…, ["localhost", "127.0.0.1"])` | Only local addresses |
| `test.py` | `os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-not-a-secret")` **before** `from .base import *` | Tests need *a* key, not a secret one. It must run before base reads it. |
| `test.py` | `PASSWORD_HASHERS = ["…MD5PasswordHasher"]` | The default hasher is deliberately slow; that's pure cost in tests. **Never** in production. |

## Tradeoffs and alternatives
- **Helpers vs. a library** (`django-environ`, `pydantic-settings`): libraries add URL parsing and type coercion. Here, 50 visible lines teach the mechanism. Swapping later is easy.
- **One settings file with `if` branches vs. a package:** branches grow into tangles; separate modules make each environment's differences explicit.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'config.settings'` | `config/settings/__init__.py` is missing | Create the empty file |
| Pages or static files can't be found after the move | `BASE_DIR` still has only two `.parent`s | Use three |
| `ImproperlyConfigured: Set the DJANGO_SECRET_KEY…` | Variable not set for this command | `DJANGO_SECRET_KEY=dev-only uv run …`, or wait for `.env` in M1.5 |
| `CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False.` | `DEBUG=false` with no hosts | Set `DJANGO_ALLOWED_HOSTS` |
