# Notes — M00.04 The professional Git loop

The full reference is [`docs/GIT_WORKFLOW.md`](../../../../docs/GIT_WORKFLOW.md). These notes cover the commands used in the lesson.

## Commands

### `gh issue create --title "…" --body-file -`
- **Where it runs:** host; creates the issue on GitHub
- **Prerequisites:** `gh auth login`

| Part | Meaning |
|---|---|
| `gh` | GitHub's official CLI |
| `issue create` | Create an issue in the repository of the current directory |
| `--title` | The issue title |
| `--body-file -` | Read the body from standard input (`-`), here a heredoc. Avoids quoting problems with long text. |

- **Expected output:** the new issue's URL.

### `git pull --ff-only`

| Part | Meaning |
|---|---|
| `git pull` | `git fetch` + integrate the remote branch into the current one |
| `--ff-only` | Only integrate if it's a fast-forward (your branch has no commits the remote lacks). Otherwise refuse, rather than create a merge commit. |

- **If it fails:** `fatal: Not possible to fast-forward, aborting.` means you committed to local `main`. Move those commits to a branch (`git switch -c rescue`), then `git switch main && git reset --hard origin/main`.

### `git switch -c docs/repo-readme-doctor`
- `-c` creates the branch at the current commit and switches to it. The older equivalent is `git checkout -b`.
- Name format: `<type>/<project>-<topic>`. Types: `feat`, `fix`, `docs`, `chore`, `hotfix`. Use `repo` as the project for repository-wide changes.

### `git add -p`

| Answer | Meaning |
|---|---|
| `y` | Stage this hunk |
| `n` | Skip it |
| `s` | Split it into smaller hunks |
| `e` | Edit the hunk by hand |
| `q` | Quit; keep what's staged so far |
| `?` | Help |

### `git diff --staged`
Shows staged changes (what the next commit will contain). Plain `git diff` shows **unstaged** changes, so it wouldn't show what you just staged.

### Commit message format

```
docs(repo): add the toolchain check to the README

New learners hit "Cannot connect to the Docker daemon" in M1.3 because
nothing told them to verify Docker first. Point them at scripts/doctor.sh
in the first section they read.

Closes #N
```

| Part | Rule |
|---|---|
| `docs` | Type: what kind of change |
| `(repo)` | Scope: which project, or `repo` |
| Subject | Imperative ("add", not "added"), ≤ 72 characters, no full stop |
| Body | Why the change exists. Wrap at about 72 columns. |
| `Closes #N` | GitHub closes the issue when this reaches `main` |

### `git push -u origin docs/repo-readme-doctor`

| Part | Meaning |
|---|---|
| `origin` | The default name of the remote you cloned from |
| `-u` | `--set-upstream`: remember that this local branch tracks `origin/docs/repo-readme-doctor`, so plain `git push` and `git pull` work later |

### `git fetch origin && git rebase origin/main`
- `fetch` downloads new commits without changing your branches.
- `rebase origin/main` replays your branch's commits on top of the latest `main`. Commit IDs change.
- **Conflicts:** fix the files, `git add <file>`, `git rebase --continue`. Abort with `git rebase --abort`.

### `git push --force-with-lease`
Overwrites the remote branch **only if** it's still where you last fetched it. Plain `--force` would silently discard commits someone else pushed in the meantime.

### `act pull_request -e pr_event.json -j repo-checks …`
See `docs/GIT_WORKFLOW.md` → "Running CI locally with act". A local run is labeled as such and isn't equivalent to a hosted run.

## Protected `main` (actual settings on the course repository)

| Rule | Value |
|---|---|
| Require a pull request | Yes, with 0 required approvals (single maintainer) |
| Include administrators | Yes |
| Require linear history | Yes |
| Require conversation resolution | Yes |
| Allow force pushes / deletion | No |
| Merge methods enabled | Squash only |

## Tradeoffs and alternatives

| Strategy | Keeps | Costs |
|---|---|---|
| Merge commit | Exact branch history | Non-linear, noisy `main` |
| Rebase and merge | Every commit, linear | Every replayed commit must work by itself |
| **Squash and merge** (default) | One commit per reviewed PR | Intermediate commits live only in the PR |

**Lesson tags vs. release tags.** Lesson tags (`lesson/MXX.YY-start|end`) are lightweight teaching markers. Note that with squash merges they point at **branch** commits, which stay reachable because the tags reference them. Release tags (`telecom/vX.Y.Z`) are annotated (`git tag -a`), point at commits on `main`, and match a CI-built image.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `remote: error: GH006: Protected branch update failed` | You pushed to `main` directly | Push a branch and open a PR |
| "Merging is blocked: unresolved conversations" | A review thread is still open | Address it, then resolve it |
| `! [rejected] … (stale info)` on `--force-with-lease` | Someone pushed to your branch since you fetched | `git fetch`, look at their commits, rebase again |
