# Exercise — M00.01 How this course works

**Start from:** a fresh clone of the course repository

## Task
You'll use checkpoint tags in every lesson. Practice now: find what changed in one lesson without watching it.

## Acceptance criteria
- [ ] `git tag -l 'lesson/*' | wc -l` prints a number greater than 0.
- [ ] You can name the files that M1.6 changed, using one `git diff` command between its two tags.
- [ ] You're on a detached `HEAD` at `lesson/M01.06-start` (`git status` says `HEAD detached at lesson/M01.06-start`), then back on `main` (`git switch main`).

## Hints
- `--stat` and `--name-only` both summarize a diff.
- Switching to a tag needs `--detach`.

## Solution
No code changes. The answer: `git diff --name-only lesson/M01.06-start lesson/M01.06-end` lists `projects/telecom/compose.yaml` (and any other file that lesson touched).
