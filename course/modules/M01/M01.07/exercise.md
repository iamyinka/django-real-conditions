# Exercise — M01.07 Management commands inside containers

**Start from:** `git switch --detach lesson/M01.07-end`, stack up

## Task
New developers keep forgetting the setup steps. Write `projects/telecom/scripts/dev-reset.sh` that rebuilds the dev environment from scratch, non-interactively, and fails loudly if any step fails.

## Acceptance criteria
- [ ] The script runs from any working directory (it changes into `projects/telecom` itself).
- [ ] It prints what it's about to destroy and refuses to continue unless it's run with `--yes`.
- [ ] Steps: `down -v`, `up -d --build`, `migrate`, create an `admin` superuser with a password read from the `DEV_ADMIN_PASSWORD` environment variable (the script fails if it's unset), then run the tests.
- [ ] `set -e` (or equivalent) is used. Break one step on purpose (an invalid `--username` flag, for example) and show the script stops there with a non-zero exit.
- [ ] Running it twice in a row works both times.

## Hints
- `cd "$(dirname "$0")/.."` moves to the project folder relative to the script's own location.

## Solution
`git diff lesson/M01.07-end solution/M01.07` (created before recording).
