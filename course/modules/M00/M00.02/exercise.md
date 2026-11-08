# Exercise — M00.02 Your toolchain, verified

**Start from:** `git switch --detach lesson/M00.02-end`

## Task
Get a clean bill of health, then prove you understand the checks by breaking one on purpose.

## Acceptance criteria
- [ ] `sh scripts/doctor.sh; echo $?` prints `All required checks passed.` and `0`.
- [ ] You can make exactly one Docker check fail **without uninstalling or stopping anything**, and the script exits `1`.
- [ ] In one sentence, you can explain why `docker version` printed a Client section in your failing run but not a Server section.

## Hints
- The Docker CLI decides which daemon to talk to. Look for an environment variable that controls it.

## Solution
`git show solution/M00.02` (created before recording). In short: `DOCKER_HOST=unix:///nonexistent.sock sh scripts/doctor.sh` fails the daemon check. The client is a local program and always answers; the server section needs a connection to the daemon, and that connection is what failed.
