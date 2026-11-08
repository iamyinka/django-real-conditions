# Storyboard — M00.04 The professional Git loop

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Diagram: the loop as a ring of 12 steps | Each step lights up as named | diagram `m0-git-loop` (from `docs/GIT_WORKFLOW.md`) | 40 |
| 2 | Terminal, then browser | `gh issue create --title "README: tell learners to run the doctor script" --body-file -` with scope + acceptance criteria; the issue page in the browser | live | 55 |
| 3 | Terminal | `git switch main` → `git pull --ff-only` → `git switch -c docs/repo-readme-doctor`; caption: `<type>/<project>-<topic>` | live | 55 |
| 4 | Terminal | `git add -p`: README hunk → `y`, typo hunk → `n`; then `git diff --staged` | live | 70 |
| 5 | Editor (commit message), then terminal | Subject `docs(repo): add the toolchain check to the README`, body highlighted; pre-commit hooks scroll by, all `Passed` | live | 55 |
| 6 | Terminal, then browser | `git push -u origin docs/repo-readme-doctor`; PR form with the template sections; `Closes #N` highlighted | live | 55 |
| 7 | Browser: Settings → Branches → rule for `main` (or `gh api` output) | Highlight: PR required, admins included, linear history, conversation resolution, force-push blocked, **approvals: 0** | live | 50 |
| 8 | Browser: PR "Files changed", a comment marked **Simulated review**, then a follow-up commit and "Resolve conversation" | Badge: **Simulated review** | live | 55 |
| 9 | Terminal: `act` run of `repo-checks` | Badge: **Run locally with act**; `Job succeeded` highlighted | live | 55 |
| 10 | Diagram: three strategies side by side, then terminal `git log --oneline -5 origin/main` | `(#7)`, `(#6)`, `(#4)` suffixes highlighted | diagram `m0-merge-strategies`; live | 70 |
| 11 | Diagram: branch replayed onto a moved `main`; terminal `git fetch origin && git rebase origin/main` → `git push --force-with-lease` | `--force-with-lease` highlighted | diagram; live | 50 |
| 12 | Terminal: `git tag -l 'lesson/M01.05*'` and (from Module 7 onward) `git tag -l 'telecom/*'` | Two columns: "lesson tags: teaching" · "release tags: deployable" | live | 55 |
| 13 | Slide | "Next: Module 1, the telecom project" | slide | 10 |

## Recording instructions
- This lesson creates a **real** issue and PR on the course repository. Make the README change genuinely useful (it's a real gap at the time of writing). The squash commit stays on `main`.
- The "unrelated typo" in scene 4 must be a real typo in another tracked file, introduced off camera **only if** none exists; it's committed separately afterwards in its own PR or discarded with `git restore`.
- Scene 8: the simulated reviewer comment is posted from the maintainer account and starts with `**Simulated review:**`.
- Scene 9: run from the repository root:
  `act pull_request -e pr_event.json -j repo-checks -P ubuntu-24.04=catthehacker/ubuntu:act-24.04 --container-architecture linux/arm64`
  If hosted Actions is available by recording day, show the hosted run instead and drop the act badge.
- Terminal 120×32, 18 px. Browser 1600×900, zoom 125%.
