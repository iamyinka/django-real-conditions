# Exercise — M01.05 Compose: Django and PostgreSQL

**Start from:** `git switch --detach lesson/M01.05-end`, then `git switch -c exercise/m1.5`

## Task
A colleague wants to use a desktop database tool against the dev database. Give them access **without** making it confusable with a Postgres already running on the host, and without exposing it to the LAN.

## Acceptance criteria
- [ ] `docker compose port db 5432` prints `127.0.0.1:5433`.
- [ ] `psql "postgresql://telecom:dev-only-change-me@127.0.0.1:5433/telecom" -c "select current_database(), inet_server_addr()"` (or any client) connects to the **container's** database, not a host Postgres.
- [ ] Django in the web container still connects with `DB_HOST=db` and `DB_PORT=5432`: `docker compose exec web python manage.py migrate` → `No migrations to apply.`
- [ ] You can explain in one sentence why `DB_PORT` stays 5432 even though you published 5433.

## Hints
- The published host port and the port containers use to talk to each other are independent.

## Solution
`git diff lesson/M01.05-end solution/M01.05` (created before recording).
