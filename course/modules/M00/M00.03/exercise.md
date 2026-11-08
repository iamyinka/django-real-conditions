# Exercise — M00.03 One repository, five independent apps

**Start from:** `git switch --detach lesson/M00.03-end`, then `git switch -c exercise/m0.3`

## Task
Module 11 will generate an OpenVPN client profile called `field-laptop.ovpn` and a Python file with a database password in it. Prove, before that happens, that neither can be committed.

## Acceptance criteria
- [ ] `git check-ignore -v projects/intranet/vpn/field-laptop.ovpn` names the rule that ignores it.
- [ ] A file `projects/intranet/settings_local.py` containing `DATABASE_URL = "postgres://admin:<a random 24-character password>@db/intranet"` is **blocked** by `uvx pre-commit run --files projects/intranet/settings_local.py`. If it isn't, add a rule to `.gitignore` that makes `git check-ignore` match it.
- [ ] `git status` is clean when you're done: no test files left behind.

## Hints
- gitleaks doesn't flag every password. Decide whether this file name should be ignored by a rule, rather than relying on the scanner alone.
- A path doesn't need to exist for `git check-ignore` to test it.

## Solution
`git diff lesson/M00.03-end solution/M00.03` (created before recording).
