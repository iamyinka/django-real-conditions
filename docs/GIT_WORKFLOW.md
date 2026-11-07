# Git workflow

This is the workflow every change in this repository follows, including the course's own work. Each step answers **what** it does, **where** it happens, and **why** we do it.

## The loop

```
issue → branch from main → small commits → local gate → push → PR → review → CI → squash merge → deploy + migrate → verify → tag
```

| Step | Where it happens | Why |
|---|---|---|
| 1. Open an issue with a business problem, scope, and acceptance criteria | GitHub | The issue records *why* the change exists. Acceptance criteria tell you when you're done. |
| 2. `git switch main && git pull --ff-only`, then `git switch -c feat/<project>-<topic>` | Your machine | Branch from an up-to-date `main`. `--ff-only` refuses to create a surprise merge commit if your local `main` has drifted. |
| 3. Commit at working milestones | Your machine | Small, reviewable steps. Each commit should leave the project runnable. |
| 4. Run the local gate: `uvx pre-commit@4.7.0 run --all-files`, the tests, and `makemigrations --check` | Your machine and the project's containers | It's cheaper to catch problems before CI does. |
| 5. `git push -u origin <branch>`, then open a PR | GitHub | The PR is where review, CI, and discussion happen. |
| 6. Review the diff, then respond to comments with new commits | GitHub | Don't force-push over a review in progress. Reviewers need to see what changed since they last looked. |
| 7. CI passes, then squash-merge | GitHub | `main` is protected. Required checks must pass. |
| 8. Deploy, run migrations, verify | Server | A merge isn't a deploy, and a deploy isn't verified until you check it. |
| 9. Tag a release when a project reaches a milestone | Your machine, then GitHub | `git tag -a telecom/v1.0.0 -m "…"`, then `git push origin telecom/v1.0.0`. |

## Protected `main`

`main` has these rules:

- Changes arrive only through a pull request, and admins can't bypass this.
- The required status checks must pass.
- History must be linear.
- Conversations must be resolved before merging.
- Force-pushing and deleting `main` are blocked.

**About approvals.** The required approval count is **0** because this course has a single maintainer, and GitHub doesn't let an author approve their own PR. Review still happens on every PR. When the course demonstrates a team scenario, the reviewer's comments are written into the PR and clearly marked **"Simulated review"**. They are never presented as coming from a real colleague. On a real team, set the required approvals to at least 1.

## Branch names

`<type>/<project>-<short-topic>`, for example `feat/telecom-ticket-dedup`, `fix/telehealth-reminder-dst`, `chore/repo-foundations`, `docs/intranet-vpn-guide`, `hotfix/telecom-outbox-retry`.

Branches are short-lived, usually hours to a few days. A long-lived branch drifts away from `main`, and the merge conflicts grow with it.

## Commit messages

```
feat(telecom): reject duplicate outage reports with an idempotency key

Retries from flaky mobile connections were creating duplicate tickets.
The client now sends an Idempotency-Key header; the server stores the key
with the first response and replays it for repeats.
```

- **Subject line:** imperative mood, at most 72 characters, as `type(scope): summary`.
- **Body:** explains *why*. The diff already shows *what* changed.
- **Staging selected changes:** use `git add -p` to stage only the hunks that belong in this commit. Unrelated edits go in their own commit.

## Merge vs. squash vs. rebase: and our default

| Strategy | Result on `main` | Good for | Cost |
|---|---|---|---|
| Merge commit | Every branch commit plus a merge commit | Keeping exact branch history | A noisy, non-linear history |
| Rebase and merge | Every branch commit, replayed onto `main` | A linear history with fine-grained commits | Each replayed commit must be runnable by itself |
| **Squash and merge** (our default) | **One commit per PR** | A clean `main` where each commit maps to one reviewed change | The branch's intermediate commits aren't kept on `main`; they remain visible in the PR |

We use squash merges for every PR. It's the only method enabled on the repository. The squash commit uses the PR title and body, so write those carefully.

**Rebase** is used for *updating your own branch*: `git fetch origin && git rebase origin/main`. Only do this before others have built on your branch. After a rebase, push with `git push --force-with-lease`. That refuses to overwrite commits on the remote that you haven't seen.

## Merge conflicts

1. `git fetch origin && git rebase origin/main`
2. Git stops at the conflicting commit. Open each conflicted file, decide what the combined result should be, and remove the conflict markers.
3. `git add <file>`, then `git rebase --continue`.
4. Run the tests again. A resolution can be free of syntax errors and still be wrong.

**Migration conflicts** are the Django-specific case. Two branches each add a `000N_…` migration to the same app, so `migrate` reports multiple leaf nodes. The fix is either `makemigrations --merge`, or, before anything has been deployed, deleting your branch's migration and regenerating it on top of `main`. Lesson M2.10 demonstrates both.

## Reverts, hotfixes, and the migration caveat

- **Revert:** `git revert <sha>` on a branch, then open a PR. This creates a new commit that undoes the code change.
- **Reverting code does not reverse database changes.** If the reverted PR added a migration that has already run in production, the database still has the new schema after the revert. Reversing it needs an explicit `migrate <app> <previous_migration>`, which may destroy data. It can also be impossible: a migration that dropped a column has thrown that data away.
- **The practical rule:** write migrations so the *previous* release of the code still works against the *new* schema. For example, add nullable columns first and remove old columns in a later release. Then rolling back the code is safe, and the database can stay where it is.
- **Hotfix:** branch from `main` as `hotfix/<project>-<topic>`, make the smallest possible fix, open a PR, merge, deploy, and tag a patch release such as `telecom/v1.0.1`.

## Tags: checkpoints and releases are separate

| Kind | Pattern | Purpose |
|---|---|---|
| Lesson checkpoint | `lesson/M05.04-start`, `lesson/M05.04-end` | Lets a learner jump to the exact code at the start or end of a lesson. |
| Exercise solution | `solution/M05.04` | Kept away from the lesson's own tags, so the answer doesn't sit next to the exercise. |
| Release | `telecom/v1.2.0` | A deployable version of a single project, using semantic versioning. |

Checkpoint tags are lightweight markers for teaching. Release tags are annotated (`git tag -a`) and correspond to a CI-built container image of the same version.

## Never commit

Secrets, `.env` files, private keys, VPN profiles, uploaded media, database files, virtual environments, or rendered video and audio. The `.gitignore`, the `detect-private-key` hook, and **gitleaks** (run locally and in CI) enforce this.

If a secret is ever committed, **rotate it immediately**. Rewriting Git history afterwards doesn't undo the exposure: the secret may already be cloned, cached, or indexed.
