## What and why
<!-- What behavior changes, and which business problem does it solve? Link the issue. -->
Closes #

## How it was validated
<!-- Commands run and their results. Say where each ran: host, container, or CI. -->
- [ ] `uvx pre-commit@4.7.0 run --all-files`
- [ ] Tests:
- [ ] Migrations: `makemigrations --check` (if models changed)
- [ ] Manual check:

## Database and deployment impact
<!-- New migrations? Are they backward compatible with the currently deployed code?
     Reverting this PR does NOT undo its migrations. Say what rollback really requires. -->

## Tradeoffs and alternatives considered

## Labels
<!-- Mark anything untested, simulated, or prepared-only. -->
