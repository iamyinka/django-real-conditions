# Exercise — M01.02 Starting from nothing

**Start from:** `git switch --detach lesson/M01.02-end`, then `git switch -c exercise/m1.2`

## Task
Operations wants a per-environment support email shown in error pages later. Add a required-in-production, optional-in-development setting `SUPPORT_EMAIL`, and an `env_int` helper for a new setting `TICKET_PAGE_SIZE` (default 25).

## Acceptance criteria
- [ ] `config/env.py` has `env_int(name, default=…)`. `TICKET_PAGE_SIZE=abc` raises `ImproperlyConfigured` with a message naming the variable; `TICKET_PAGE_SIZE=` (empty) uses the default.
- [ ] `base.py` reads `SUPPORT_EMAIL` as required. `dev.py` gives it a default (`support@localhost`), so `DJANGO_SECRET_KEY=x uv run python manage.py check` still passes in dev.
- [ ] `DJANGO_SETTINGS_MODULE=config.settings.base DJANGO_SECRET_KEY=x uv run python manage.py check` fails with `Set the SUPPORT_EMAIL environment variable.`
- [ ] New tests cover `env_int`: valid value, empty value → default, non-numeric → error. `uv run pytest` passes.

## Hints
- In `dev.py`, the default needs to be in place *before* base reads the variable, or dev must read the variable again after the star import. Pick one and explain why in a comment.

## Solution
`git diff lesson/M01.02-end solution/M01.02` (created before recording).
