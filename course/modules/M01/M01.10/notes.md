# Notes — M01.10 Shipping the skeleton: first issue, branch, and PR

## Commands

### `git add <path>` vs. `git add .` vs. `git add -p`

| Command | Stages | Risk |
|---|---|---|
| `git add .` | Everything changed or new under the current directory (respecting `.gitignore`) | Sweeps in scratch files and debug edits |
| `git add <path>` | That file, entirely | |
| `git add -p [<path>]` | Interactively, hunk by hunk | Slower, precise |

### `git diff main...HEAD --stat`

| Form | Meaning |
|---|---|
| `git diff A..B` | Difference between the tips of A and B (includes changes `main` made since you branched) |
| `git diff A...B` | Difference between the **merge base** of A and B, and B: only what your branch changed. This is what GitHub's "Files changed" shows. |
| `--stat` | Per-file summary |

### `git push origin 'refs/tags/lesson/*'`
- Plain `git push` doesn't send tags.
- `refs/tags/lesson/*` is a refspec pattern; the quotes stop the shell from expanding `*`.
- `git push --tags` would send **every** local tag, including experiments. Pushing by pattern is deliberate.
- **Verify:** `git ls-remote --tags origin 'lesson/*' | wc -l` → `16` at this point.

### `git switch main && git pull --ff-only && git branch -d feat/telecom-skeleton`
- `git branch -d` refuses to delete a branch that isn't merged. After a **squash** merge, Git may consider it unmerged (the commits differ). If you've confirmed the PR was merged on GitHub, use `-D`.

### `git merge-base --is-ancestor A B; echo $?`
Exit 0 if A is in B's history, 1 if not. After squash-merging, the branch's commits (and the lesson tags on them) aren't ancestors of `main`.

### `git diff --quiet lesson/M01.09-end 6b794b4 -- projects/telecom && echo identical`
`--quiet` suppresses output and sets the exit status: 0 = no differences. Proves the squash commit contains exactly the reviewed end state.

## The PR description (PR #4, abridged)

| Section | Content | Why |
|---|---|---|
| Title | `feat(telecom): runnable Django 6.1 + Postgres 18 skeleton (Module 1 code)` | Becomes the squash commit's subject |
| What | Table of lessons, commit SHAs, what each adds | Reviewers can go commit by commit |
| `Closes #3` | Links and auto-closes the issue | |
| Why | One paragraph | |
| Verification | pre-commit, gitleaks, 16 tests, behavior checks | Claims backed by evidence |
| Honesty line | "CI hasn't run on GitHub… these checks ran locally" | Never imply a check ran when it didn't |
| Notes for the reviewer | Tag reachability after squash; pytest-django doesn't declare Django 6.1 | Known caveats up front |

## Responding to review

| Do | Don't |
|---|---|
| Push new commits that address comments | Force-push a rewrite mid-review |
| Reply with what you changed **and how you verified it** | Reply "done" |
| Resolve a thread once it's addressed | Leave threads open (`main` requires resolution) |
| Push back with evidence when you disagree | Silently ignore a comment |

## Tradeoffs and alternatives
- **Lesson tags on branch commits** keep per-lesson history after squashing. The alternative, rebase-merging to keep every commit on `main`, would require each lesson commit to stand alone and would clutter `main` with teaching steps.
- **One big PR vs. one per lesson:** per-lesson PRs are easier to review; here, the issue scoped Module 1 as one deliverable. On a team, prefer smaller PRs.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `error: The branch 'feat/…' is not fully merged.` after a squash merge | Squash created a different commit | Confirm on GitHub, then `git branch -D` |
| Tags missing on GitHub | Tags weren't pushed | `git push origin 'refs/tags/lesson/*'` |
| "Merging is blocked" | Unresolved conversation or a failing required check | Resolve threads; fix checks |
| The squash commit has a messy message | The PR title/body was edited poorly | Edit the title before merging; it's the commit subject |
