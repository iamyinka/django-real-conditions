# Storyboard — M01.10 Shipping the skeleton: first issue, branch, and PR

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Terminal: `git log --oneline main..feat/telecom-skeleton` (8 commits); issue #3 | Lesson tags beside each commit | repo at `lesson/M01.10-start` | 45 |
| 2 | Terminal | `git status` (README.md modified, `scratch.txt` untracked, `config/settings/dev.py` modified with `print(...)`); `git add projects/telecom/README.md`; `git add -p config/settings/dev.py` → `n`; `git restore config/settings/dev.py`; `rm scratch.txt`; `git diff --staged` | live (scripted setup) | 80 |
| 3 | Terminal | `git diff main...HEAD --stat` → `28 files changed, 922 insertions(+)`; scrolling `git diff main...HEAD` | live | 60 |
| 4 | Terminal | `uvx pre-commit@4.7.0 run --all-files` (all Passed); `docker run --rm -v "$PWD:/repo" ghcr.io/gitleaks/gitleaks:v8.30.1 git /repo --redact` → `no leaks found`; `docker compose exec web pytest -q` → `16 passed`; check + makemigrations --check | live | 70 |
| 5 | Terminal | `git push -u origin feat/telecom-skeleton`; `git push origin 'refs/tags/lesson/*'`; `git ls-remote --tags origin 'lesson/*' \| wc -l` → `16` | live | 45 |
| 6 | Browser: PR #4 description | Lesson table, `Closes #3`, Verification section, "CI hasn't run on GitHub" line | `iamyinka/django-real-conditions#4` | 70 |
| 7 | Browser: two review threads, badge **Simulated review**; terminal shows the `/data` test (exit 1) | Thread 1 → reply + resolve; thread 2 → new commit fixing the compose comment, reply with the result | recorded review on a re-run PR (see instructions) | 90 |
| 8 | Terminal: `act` run, badge **Run locally with act** | `Job succeeded` | live | 40 |
| 9 | Browser: "Squash and merge" → merged; terminal `git switch main && git pull --ff-only && git branch -d feat/telecom-skeleton`; `git log --oneline -3` → `6b794b4 feat(telecom): runnable Django 6.1 + Postgres 18 skeleton (Module 1 code) (#4)` | `(#4)` highlighted | browser; live | 60 |
| 10 | Terminal | `git merge-base --is-ancestor lesson/M01.09-end origin/main; echo $?` → `1`; `git switch --detach lesson/M01.05-end` works; `git diff --quiet lesson/M01.09-end 6b794b4 -- projects/telecom && echo identical` → `identical` | live | 65 |
| 11 | Slide: Module 1 recap | Empty folder → reviewed skeleton on protected `main` | slide | 30 |

## Recording instructions
- PR #4 was merged on 2026-11-08 without the review threads shown in scene 7. To record scene 7 honestly, **re-run it**: from `lesson/M01.10-start`, push a fresh branch `feat/telecom-skeleton-demo`, open a draft PR, post the two comments marked `**Simulated review:**`, do the fix commit, then **close** the demo PR without merging. Say on screen that the merged PR is #4 and the review shown is a re-enactment.
- The comment fix in scene 7 really happened on 2026-11-07, when testing showed the old `/data` path exits 1 with a message rather than failing silently. The re-enactment reproduces that correction.
- Scene 2's untidy working tree is set up off camera: append `print("debug")` to `config/settings/dev.py` and create `scratch.txt`.
- Verified 2026-11-08: PR #4 had 8 commits; the squash commit `6b794b4` changed 28 files with 922 insertions; the remote branch is deleted; `lesson/M01.09-end` isn't an ancestor of `main`, and its `projects/telecom` tree is identical to `6b794b4`'s.
