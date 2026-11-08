# M00.03 — One repository, five independent apps

- **Target length:** 12 min
- **Checkpoint at start:** `lesson/M00.02-end`
- **Checkpoint at end:** `lesson/M00.03-end` (no code changes)
- **Prerequisites:** M0.2 (toolchain verified); a clone of the course repository
- **Working directory:** the repository root
- **Labels:** Simulated (the leaked token in scene 7 is fake, generated for the demo)

## Learning goal
Find your way around the course repository, explain why the five projects share a repository but not code, and prove that secrets, databases, media and virtual environments can't be committed by accident.

## Script

### Scene 1 — The top level

Let's open the repository and look at the top level.
There are five folders that matter.
Projects holds the five applications.
Course holds the lesson scripts, notes, exercises, and the version list.
Docs holds how we work: the Git workflow and the review rules.
Scripts and tools hold small helpers, like the doctor script from the last lesson.
And dot github holds the pull request template, issue forms, and the CI workflow.
> spoken: And dot GitHub holds the pull request template, issue forms, and the C I workflow.

---

### Scene 2 — Why one repository

Why put five apps in one repository?
For a course, it means one clone, one history, and one set of checkpoint tags to follow.
Teams do this too, and it's called a monorepo.
> spoken: Teams do this too, and it's called a mono repo.
It makes changes that touch several projects reviewable in one pull request.
But one repository doesn't mean one application.
That distinction drives the whole layout.

---

### Scene 3 — Independent projects

Open projects, then telecom.
> spoken: Open projects, then telecom.
It has its own dependency list in pyproject dot toml, its own lock file, its own Dockerfile, and its own compose file.
> spoken: It has its own dependency list in pie project dot toml, its own lock file, its own Dockerfile, and its own compose file.
Each project you'll build gets the same set.
You can start, stop, upgrade, or delete one project without touching the others.
The telehealth app can move to a newer library while telecom stays put.
Each project also gets its own release tags, like telecom slash v one point zero point zero.
> spoken: Each project also gets its own release tags, like telecom, version one point oh point oh.

---

### Scene 4 — Shared code stays small

So where does shared code go?
Mostly, nowhere.
When two projects need the same idea, like a health check, each project gets its own small copy.
That sounds wasteful, and sometimes it is.
But shared code couples projects together: change it for one, and you've changed it for all five.
In a course, coupling makes every lesson depend on every other lesson.
At work, it means a change for one team can break another team's deploy.
The rule here: copy small things, and only share code when the duplication is clearly costing more than the coupling.

---

### Scene 5 — What never gets committed

Some files must never go into Git.
Secrets, like passwords, API keys, and private keys.
> spoken: Secrets, like passwords, A P I keys, and private keys.
Local databases.
Uploaded media.
Virtual environments, which are large, and built for your operating system, not anyone else's.
And rendered videos, which are huge and change constantly.
The file that enforces this is dot gitignore at the repository root.
> spoken: The file that enforces this is dot git ignore at the repository root.

---

### Scene 6 — Proving the ignore rules

Don't trust an ignore file; test it.
I'll create a dot env file in the telecom project, the kind of file that holds real secrets.
> spoken: I'll create a dot env file in the telecom project, the kind of file that holds real secrets.
Run git status.
It doesn't appear.
To find out why, run git check-ignore with the verbose flag, and the path.
> spoken: To find out why, run git check ignore with the dash V flag, and the path.
Git prints the exact rule that matched, and the line number in dot gitignore.
> spoken: Git prints the exact rule that matched, and the line number in dot git ignore.
Now try the same command on the example file, dot env dot example.
> spoken: Now try the same command on the example file, dot env dot example.
Nothing prints.
That file is already committed, and ignore rules never apply to files Git is already tracking.
That's worth remembering: adding a rule doesn't un-commit anything.
To test the rules alone, add the no-index flag.
> spoken: To test the rules alone, add the dash dash no index flag.
Now Git shows the rule with an exclamation mark: an exception that keeps the example file out of the ignore list.
It's committed on purpose, with a harmless placeholder for every setting.

---

### Scene 7 — When a secret slips through

Ignore rules only cover files you planned for.
What if someone pastes a token straight into a settings file?
This token is fake, generated for this demo, but it has the shape of a real GitHub token.
I'll stage the file, and run the commit checks.
The secret scanner, gitleaks, fails and points at the file and the line.
> spoken: The secret scanner, git leaks, fails and points at the file and the line.
The commit doesn't happen.
These checks run on every commit through a tool called pre-commit, and the same scanner runs again in CI, in case someone skipped the local hooks.
> spoken: These checks run on every commit through a tool called pre commit, and the same scanner runs again in C I, in case someone skipped the local hooks.

---

### Scene 8 — Why "just delete it" isn't enough

Here's why blocking matters so much.
If a secret does get committed, deleting the file in the next commit doesn't remove it.
It's still in the history, and anyone with a clone can find it.
On a public repository, automated scanners find leaked keys within minutes.
The only real fix is to revoke the secret and issue a new one.
Rewriting history comes second, and it doesn't help with copies that already exist.

---

### Scene 9 — Line endings and editor settings

Two more small files at the root.
Dot gitattributes tells Git to store text files with Unix line endings.
> spoken: Dot git attributes tells Git to store text files with Unix line endings.
Without it, a shell script checked out on Windows can gain hidden carriage returns and fail inside a Linux container with a confusing error.
And dot editorconfig gives every editor the same indentation and final-newline settings, so diffs stay clean.
> spoken: And dot editor config gives every editor the same indentation and final newline settings, so diffs stay clean.

---

### Scene 10 — Next

That's the layout.
Next, we'll put it to work with the professional Git loop: issue, branch, commits, pull request, review, merge, and tags.
