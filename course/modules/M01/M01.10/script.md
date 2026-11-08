# M01.10 — Shipping the skeleton: first issue, branch, and PR

- **Target length:** 14 min
- **Checkpoint at start:** `lesson/M01.10-start` (= `lesson/M01.09-end`)
- **Checkpoint at end:** `lesson/M01.10-end` (= the squash commit on `main`)
- **Prerequisites:** M0.4, M1.1–M1.9
- **Working directory:** the repository root
- **Labels:** Simulated (review comments in scene 7). CI is "run locally with act" until hosted Actions is available.

## Learning goal
Take a multi-lesson branch through review to `main`: stage only what belongs, review your own diff, write a PR that proves its claims, respond to review, squash-merge, and confirm what survives on `main` and in the tags.

## Script

### Scene 1 — Where we are

Module one's work lives on one branch: feature slash telecom skeleton.
> spoken: Module one's work lives on one branch: feature, telecom skeleton.
Eight commits, one per lesson, each tagged.
It's linked to the issue we wrote in lesson one.
None of it is on main yet.
This lesson is the last mile: getting reviewed work onto main, properly.

---

### Scene 2 — Only what belongs

Before the final commit, look at git status.
There's the README change we want, and two things we don't.
> spoken: There's the read me change we want, and two things we don't.
A scratch file with some notes, and a debugging print I left in a settings file.
git add with a dot would sweep all of it in.
> spoken: Git add with a dot would sweep all of it in.
Instead, stage the README by name.
> spoken: Instead, stage the read me by name.
For the settings file, use git add, dash p, and answer no to the print statement.
> spoken: For the settings file, use git add, dash P, and answer no to the print statement.
Then remove the print, and delete the scratch file.
git diff, staged, shows exactly the change we meant.
> spoken: Git diff, staged, shows exactly the change we meant.

---

### Scene 3 — Review your own diff first

Now step back and look at the whole branch the way a reviewer will.
git diff main, three dots, HEAD, with the stat flag.
> spoken: Git diff main, three dots, head, with the stat flag.
Three dots means: what this branch changed since it split from main, ignoring anything main did meanwhile.
Twenty-eight files.
Scan the list for anything that shouldn't be there: a dot env file, a database, a virtual environment.
> spoken: Scan the list for anything that shouldn't be there: a dot env file, a database, a virtual environment.
None.
Then read the full diff, file by file, before anyone else has to.

---

### Scene 4 — The local gate

Run the checks a reviewer would ask about.
Pre-commit on all files: every hook passes.
> spoken: Pre commit on all files: every hook passes.
The secret scanner over the whole history: no leaks found.
The tests, in the container: sixteen passed.
And the system check, and makemigrations check: clean.
> spoken: And the system check, and make migrations check: clean.
Each result goes into the pull request description, as evidence.

---

### Scene 5 — Push branch and tags

Push the branch with dash u.
> spoken: Push the branch with dash U.
Tags don't travel with a normal push, so push them explicitly.
Push origin, then the refs slash tags slash lesson pattern, in quotes so the shell leaves the star alone.
> spoken: Push origin, then the lesson tags, by pattern, in quotes so the shell leaves the star alone.
Sixteen lesson tags are now on GitHub.

---

### Scene 6 — A pull request that proves itself

Open the pull request.
The title follows the commit format, because with squash merging, the title becomes the commit message on main.
The body has a table: lesson, commit, and what it adds.
Closes, and the issue number.
> spoken: Closes, and the issue number.
A verification section, with every check we just ran.
And one honest line: hosted CI hasn't run, because Actions is unavailable on this account, so the checks were run locally.
> spoken: And one honest line: hosted C I hasn't run, because Actions is unavailable on this account, so the checks were run locally.
A reviewer should never have to guess what was tested.

---

### Scene 7 — Review

Now the review, and this one is labeled simulated: I'm writing the reviewer's comments myself, playing a colleague.
First comment: the compose file binds web to localhost only; is that intentional?
Yes, and the comment in the file already says why, so I reply with a link to those lines, and resolve it.
Second comment: what happens if someone copies the old Postgres volume path from a tutorial?
That's a good catch, and a real gap: the comment said it would fail silently.
I tested it: it doesn't fail silently; it exits with code one and a clear message.
So I fix the comment, in a new commit on the same branch, and reply with the test result.
New commits, not a rewrite, so the reviewer can see exactly what changed since they last looked.

---

### Scene 8 — CI

The CI workflow runs pre-commit and the secret scanner on a clean machine.
> spoken: The C I workflow runs pre commit and the secret scanner on a clean machine.
Here it runs locally with act, and the label says so.
When hosted Actions is available, this same workflow runs on GitHub, and becomes a required check.

---

### Scene 9 — Squash and merge

All conversations resolved, checks green.
Squash and merge.
Eight commits become one, with the PR title as the subject.
GitHub closes the issue, and deletes the branch.
On your machine: switch to main, pull with fast forward only, and delete the local branch.
> spoken: On your machine: switch to main, pull with fast forward only, and delete the local branch.
git log on main: one new line, ending with the PR number.
> spoken: Git log on main: one new line, ending with the P R number.

---

### Scene 10 — Do the tags still work?

The branch is gone, so are the lesson tags broken?
Ask Git: is lesson M one point oh nine end an ancestor of main?
> spoken: Ask Git: is lesson M oh one point oh nine end an ancestor of main?
No. Squashing created a brand-new commit, so the branch commits aren't part of main's history.
But they still exist, because the tags point at them, and Git keeps anything a tag references.
Switch to any lesson tag, and it works.
And here's the check that matters: compare the telecom folder at the last lesson tag with the squash commit on main.
No differences.
The tags preserve the steps; main preserves the result.

---

### Scene 11 — Module one complete

Module one is done.
We started from an empty folder, and ended with a reviewed, containerized Django skeleton on a protected main branch.
In Module two, we model the business: customers, sites, subscriptions, and tickets.
