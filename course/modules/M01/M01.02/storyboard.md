# Storyboard — M01.02 Starting from nothing

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Terminal: `ls -a projects/telecom` (empty) | "Goal: refuse to start without a secret" | `lesson/M01.02-start` | 20 |
| 2 | Terminal, then editor | `uv init --bare --python 3.14 --name telecom` → `pyproject.toml` (`requires-python = ">=3.14"`); `uv add django==6.1.3` → `pyproject.toml` dependency line, `uv.lock` head, `.venv/` | live | 90 |
| 3 | Terminal + file tree | `uv run django-admin startproject config .`; tree shows `manage.py`, `config/{settings.py,urls.py,wsgi.py,asgi.py}` | live | 55 |
| 4 | Editor: `manage.py` | Highlight `os.environ.setdefault("DJANGO_SETTINGS_MODULE", …)` and `execute_from_command_line(sys.argv)` | `manage.py:9-18` | 60 |
| 5 | Editor: generated `settings.py` | Highlight `SECRET_KEY = 'django-insecure-…'` and `DEBUG = True` (red) | generated file | 45 |
| 6 | File tree morph `settings.py` → `settings/{base,dev,test}.py`; editor on `dev.py` and `test.py` | `from .base import *`; `DEBUG = env_bool("DJANGO_DEBUG", True)`; `PASSWORD_HASHERS = [MD5]`; `pyproject.toml` `DJANGO_SETTINGS_MODULE = "config.settings.test"` | `config/settings/*.py` at `-end` | 70 |
| 7 | Editor: `config/env.py` | `env` (lines 19–31), `env_bool` (34–44), `env_list` (47–51), one at a time | `config/env.py` | 85 |
| 8 | Diagram: timeline "import settings → checks → serve requests"; the error stops it at the first box | "Fail at startup, not at 3 a.m." | diagram `m1-import-time` | 35 |
| 9 | Terminal, then browser | `uv run python manage.py check` → `ImproperlyConfigured: Set the DJANGO_SECRET_KEY environment variable.`; `DJANGO_SECRET_KEY=x DJANGO_DEBUG=ture …` → `DJANGO_DEBUG must be true or false, got 'ture'.`; `DJANGO_SECRET_KEY=dev-only uv run python manage.py check` → `System check identified no issues (0 silenced).`; `… runserver` → browser at `localhost:8000`, "The install worked successfully!" | live | 90 |
| 10 | Editor `tests/test_env.py`, then terminal | `uv run pytest` → `10 passed` | `tests/test_env.py` | 40 |
| 11 | Slide | "Next: the Dockerfile" | slide | 10 |

## Recording instructions
- Record from `lesson/M01.02-start`, typing the commands. Scene 6's refactor is a cut: show the before tree, then the `-end` files. Don't type it live.
- Outputs verified 2026-11-08 at `lesson/M01.02-end` (uv 0.13.7, Django 6.1.3, Python 3.14.2 on the host): the three `check` results above, `10 passed in 0.04s`, and `GET / 200` from runserver.
- The browser shows `http://localhost:8000/` at 1600×900.
