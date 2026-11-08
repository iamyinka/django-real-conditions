# Exercise — M01.09 Non-root containers, permissions, and secrets

**Start from:** `git switch --detach lesson/M01.09-end`, then `git switch -c exercise/m1.9`

## Task
Move the database password out of the environment for the **db** service, using Compose secrets, and prove the difference.

## Acceptance criteria
- [ ] `compose.yaml` defines a secret `db_password` from a git-ignored file `secrets/db_password.txt`. The Postgres image reads it via `POSTGRES_PASSWORD_FILE=/run/secrets/db_password`.
- [ ] `docker compose exec db env | grep POSTGRES_PASSWORD=` prints nothing; `docker compose exec db cat /run/secrets/db_password` prints the value.
- [ ] `git check-ignore -v projects/telecom/secrets/db_password.txt` names a rule. Check whether an existing rule already covers it before you add one.
- [ ] Web still connects (its `POSTGRES_PASSWORD` comes from `.env`), and `/readyz` returns 200 after `docker compose down -v && docker compose up -d`.
- [ ] In two sentences: what does this protect against, and what doesn't it protect against?

## Hints
- The Postgres image documents `_FILE` variants for its `POSTGRES_*` variables.

## Solution
`git diff lesson/M01.09-end solution/M01.09` (created before recording).
