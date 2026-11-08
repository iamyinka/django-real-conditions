# Exercise — M00.04 The professional Git loop

**Start from:** your own fork of the course repository (GitHub → Fork), cloned locally at `main`

## Task
Run the whole loop once in your fork, end to end, on a tiny change: add a "My setup" section to `README.md` with the output of `sh scripts/doctor.sh` from your machine.

## Acceptance criteria
- [ ] An issue in your fork describes the change, with at least one acceptance criterion.
- [ ] Your fork's `main` is protected: a direct `git push origin main` is rejected.
- [ ] The branch name follows `<type>/<project>-<topic>`.
- [ ] The PR contains exactly the README change. `git show --stat` on the squash commit lists only `README.md`.
- [ ] The PR body says `Closes #<issue>`, and the issue closed automatically when you merged.
- [ ] `git log --oneline -1 origin/main` shows your PR's title ending in `(#<PR number>)`.

## Hints
- Branch protection is under Settings → Branches (or Rules → Rulesets) in your fork.
- Turn off "Allow merge commits" and "Allow rebase merging" in Settings → General to match the course repository.

## Solution
There's no code solution tag for this exercise. The acceptance criteria are checkable in your fork.
