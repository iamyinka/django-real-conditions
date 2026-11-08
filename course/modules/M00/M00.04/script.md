# M00.04 — The professional Git loop

- **Target length:** 14 min
- **Checkpoint at start:** `lesson/M00.03-end`
- **Checkpoint at end:** `lesson/M00.04-end` (no project code changes; the demo PR edits `README.md`)
- **Prerequisites:** M0.3; a GitHub account; `gh` logged in for the demo (optional for learners)
- **Working directory:** the repository root
- **Labels:** Simulated (review comment in scene 8). CI shown is "run locally with act" until hosted Actions is available on the recording account.

## Learning goal
Run the full loop (issue, branch, commits, local checks, pull request, review, CI, squash merge, tag) and explain why `main` is protected, why squash merge is the default, and how lesson tags differ from release tags.

## Script

### Scene 1 — The loop

Every change in this course, including the course's own work, goes through the same loop.
Issue, branch, commits, local checks, push, pull request, review, CI, merge, deploy, verify, and tag.
> spoken: Issue, branch, commits, local checks, push, pull request, review, C I, merge, deploy, verify, and tag.
It looks like a lot of ceremony for a small change.
Each step exists because skipping it has burned someone.
We'll walk through it once with a real, small change, so later lessons can just say "open a PR".
> spoken: We'll walk through it once with a real, small change, so later lessons can just say "open a P R".

---

### Scene 2 — Start with an issue

Start on GitHub, with an issue.
The issue says why the change exists: a problem, the scope, and acceptance criteria.
Acceptance criteria are checks you can actually run, so "done" isn't a matter of opinion.
Ours is small: the README doesn't tell new learners to run the doctor script.
> spoken: Ours is small: the read me doesn't tell new learners to run the doctor script.
I'll create it from the terminal with the GitHub command-line tool, but the website works just as well.

---

### Scene 3 — Branch from an up-to-date main

Now the branch.
First, switch to main and pull with the fast-forward-only flag.
> spoken: First, switch to main and pull with the dash dash F F only flag.
That flag refuses to create a surprise merge commit if your local main has drifted from GitHub.
Then create the branch with git switch, dash c, and a name.
> spoken: Then create the branch with git switch, dash C, and a name.
Branch names follow a pattern: the type of change, a slash, the project, and a short topic.
Docs slash repo, readme doctor.
> spoken: Docs, slash, repo readme doctor.
Branches live for hours or days, not weeks.
The longer a branch lives, the further it drifts from main, and the bigger the merge conflicts get.

---

### Scene 4 — Commit only what belongs together

I've edited the README, and I've also fixed an unrelated typo in another file.
> spoken: I've edited the read me, and I've also fixed an unrelated typo in another file.
Those are two different changes.
Run git add with the patch flag.
> spoken: Run git add with the dash P flag.
Git shows each change, one hunk at a time, and asks whether to stage it.
Yes to the README hunk; no to the typo.
> spoken: Yes to the read me hunk; no to the typo.
Now git diff, with the staged flag, shows exactly what this commit will contain.
> spoken: Now git diff, with the dash dash staged flag, shows exactly what this commit will contain.
Read it.
Reviewing your own diff before anyone else does is the cheapest review there is.

---

### Scene 5 — A commit message that explains why

The commit message has a subject and a body.
The subject is short and imperative: docs, in brackets repo, add the toolchain check to the README.
> spoken: The subject is short and imperative: docs, repo, add the toolchain check to the read me.
The body explains why.
The diff already shows what changed; nobody can recover your reasoning from it later.
When I commit, the pre-commit checks run: whitespace, file formats, Python lint, and the secret scanner.
> spoken: When I commit, the pre commit checks run: whitespace, file formats, Python lint, and the secret scanner.
They pass, and the commit is recorded.

---

### Scene 6 — Push and open the pull request

Push the branch with git push, dash u, origin, and the branch name.
> spoken: Push the branch with git push, dash U, origin, and the branch name.
The dash u flag remembers the link, so later pushes are just git push.
> spoken: The dash U flag remembers the link, so later pushes are just git push.
Then open a pull request.
The template asks for what changed, why, and how it was verified, and it links the issue.
Writing "closes" and the issue number means merging the PR will close the issue automatically.
> spoken: Writing "closes" and the issue number means merging the P R will close the issue automatically.

---

### Scene 7 — Protected main

Why not just push to main?
Because main is protected.
Changes only arrive through a pull request, and even the repository's admin can't bypass that.
History must stay linear, every conversation must be resolved, and force-pushing to main is blocked.
> spoken: History must stay linear, every conversation must be resolved, and force pushing to main is blocked.
One honest detail about this repository: the required approval count is zero.
The course has one maintainer, and GitHub doesn't let you approve your own pull request.
On a real team, set it to at least one.

---

### Scene 8 — Review

So review here means reading the diff on GitHub as if someone else wrote it.
When the course shows a team scenario, reviewer comments are written into the pull request and marked as a simulated review.
Here's one: it asks for the expected output to be shown, not just the command.
I answer with a new commit on the same branch, rather than rewriting the old one.
That way the reviewer sees exactly what changed since they last looked.
Then I resolve the conversation.

---

### Scene 9 — CI

CI runs the same checks again, on a clean machine.
> spoken: C I runs the same checks again, on a clean machine.
It catches anything that only worked on my laptop, and anyone who skipped the local hooks.
Right now, hosted CI is unavailable on the account I'm recording with, so this run is a local one, using a tool called act.
> spoken: Right now, hosted C I is unavailable on the account I'm recording with, so this run is a local one, using a tool called act.
The label on screen says so.
A local run uses a different machine image and network, so it's evidence, not a replacement.
Module seven sets up hosted CI properly.
> spoken: Module seven sets up hosted C I properly.

---

### Scene 10 — Merge, rebase, or squash

Time to merge, and GitHub offers three ways.
A merge commit keeps every branch commit plus an extra commit joining them.
Rebase and merge replays each branch commit onto main, one by one.
Squash and merge turns the whole pull request into one commit on main.
This repository allows only squash merges.
Each commit on main then matches one reviewed change, with the PR title and description as its message.
> spoken: Each commit on main then matches one reviewed change, with the P R title and description as its message.
The small steps aren't lost; they stay visible in the pull request.
Run git log on main, and you'll see one line per pull request, each ending with its number.

---

### Scene 11 — Updating your branch with rebase

Rebase still has a job: updating your own branch while main moves on.
Fetch, then rebase onto origin main.
> spoken: Fetch, then rebase onto origin main.
Your commits are replayed on top of the latest main.
Because that rewrites your branch, the next push must be forced, and the safe way is the force with lease flag.
> spoken: Because that rewrites your branch, the next push must be forced, and the safe way is the dash dash force with lease flag.
It refuses to overwrite commits on GitHub that you haven't seen yet.
Only do this on a branch nobody else is building on.

---

### Scene 12 — Two kinds of tags

The loop ends with tags, and this course uses two kinds.
Lesson tags, like lesson slash M one point oh five dash end, mark the code at the start and end of each lesson.
> spoken: Lesson tags, like lesson M oh one point oh five end, mark the code at the start and end of each lesson.
They're for learning.
Release tags, like telecom slash v one point oh point oh, mark a version you'd actually deploy.
> spoken: Release tags, like telecom version one point oh point oh, mark a version you'd actually deploy.
They're annotated, with a message, and each one matches a container image built by CI.
And between merge and tag sit two steps we'll practice in Module seven: deploy, then verify.
A merge isn't a deploy, and a deploy isn't done until you've checked it.

---

### Scene 13 — Next

That's the whole loop.
In Module one, we start the telecom project, and every lesson's code goes through exactly this process.
