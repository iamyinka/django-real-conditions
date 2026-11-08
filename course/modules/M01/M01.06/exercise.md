# Exercise — M01.06 Volumes

**Start from:** `git switch --detach lesson/M01.06-end`, with the stack up and migrated

## Task
Before Module 7 teaches proper backups, prove you can move data between two databases using only volumes and Postgres tools.

## Acceptance criteria
- [ ] Create a table `ticket_demo` with three rows in the telecom database.
- [ ] Produce a dump file **on your host** with `docker compose exec db pg_dump …`, redirected to a file. `head` shows `CREATE TABLE public.ticket_demo`.
- [ ] Run `docker compose down -v`, then `up -d`. Show the table is gone.
- [ ] Restore the dump with `docker compose exec -T db psql …` reading the file on stdin. `select count(*) from ticket_demo` returns 3.
- [ ] In one sentence: why does the restore command need `-T`?

## Hints
- `exec` allocates a terminal by default, and a terminal and piped stdin don't mix.

## Solution
`git show solution/M01.06:course/solutions/M01.06.md` (created before recording).
