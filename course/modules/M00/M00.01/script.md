# M00.01 — How this course works

- **Target length:** 8 min
- **Checkpoint at start:** none (first lesson)
- **Checkpoint at end:** `lesson/M00.01-end` (the repository as cloned)
- **Prerequisites:** none
- **Working directory:** none
- **Labels:** none

## Learning goal
Know what the five projects are, what "real conditions" means in this course, and how to use the WHAT / WHERE / WHY habit, the honesty labels, checkpoint tags, and exercises.

## Script

### Scene 1 — The gap

Most Django tutorials end when the page loads on your laptop.
Real work starts after that.
A technician loses signal in a basement and taps "save" three times.
Two dispatchers assign the same technician at the same second.
A deploy goes out, and nobody ran the migration.
This course is about that part: Django when the conditions aren't friendly.

---

### Scene 2 — Five projects

You'll build five separate applications, each one a different kind of business.
First, a telecom field-service app, where technicians work offline and sync when they can.
Second, a telehealth platform, with appointments, private documents, and video calls.
Third, a streaming service for learners on slow, expensive connections.
Fourth, a lab logistics app that tracks specimens and live courier locations.
And fifth, a private intranet that's only reachable over the office network or a VPN.
> spoken: And fifth, a private intranet that's only reachable over the office network or a V P N.
Each project introduces new problems, and each one reuses what the earlier projects taught.
The first project gets the most time, because that's where the foundations go in.

---

### Scene 3 — What "real conditions" means

Real conditions means three things here.
The code runs the way teams run it: in containers, from a Git repository, through pull requests.
Failures are part of the lesson: we break things on purpose, read the error, and fix it.
And every claim is checked: if I say a command does something, you'll see it do it.

---

### Scene 4 — WHAT, WHERE, WHY

Every command and every block of code in this course comes with three answers.
What does it do?
Where does it run?
And why are we doing it this way?
"Where" is the one most tutorials skip, and it causes the most confusion.
Take this command.
docker compose exec web python manage.py migrate.
> spoken: docker compose exec web python manage dot py migrate.
You type it on your machine.
Docker runs the Python part inside the web container.
And the tables it changes live in a third place: the database container.
Three places, one line.
If you ever feel lost, ask yourself those three questions, and you'll usually find your footing.

---

### Scene 5 — Honesty labels

Some things in this course can't be real on a laptop.
There's no real SMS provider, no real patients, and no real GPS fleet.
> spoken: There's no real S M S provider, no real patients, and no real G P S fleet.
When something is a stand-in, you'll see a label on screen.
Simulated means we built a fake on purpose, like an SMS gateway that fails when we tell it to.
> spoken: Simulated means we built a fake on purpose, like an S M S gateway that fails when we tell it to.
Prepared-only means I'll show you the configuration, but we won't run it in the recording.
Hypothesis means it's a reasonable expectation that we haven't measured yet.
If there's no label, it ran, and what you see is what happened.

---

### Scene 6 — Checkpoints and exercises

The code lives in one public Git repository.
Every lesson that changes code has two tags: where the lesson starts, and where it ends.
If you get stuck or fall behind, check out the start tag and carry on from there.
When you finish, compare your work with the end tag, and the differences will show you exactly what you missed.
Most lessons end with an exercise.
Each exercise has acceptance criteria: specific checks that tell you when you're done.
The solutions sit on separate tags, so you won't see them by accident.
Try the exercise before you look.

---

### Scene 7 — Mistakes on purpose

Here's a taste of what "failures are part of the lesson" looks like.
This is a real error from Module 1.
Connection refused, on port five four three two.
The settings say the database is at localhost.
Inside a container, localhost means the container itself, and there's no database in there.
You'll make this mistake on purpose, read the message, and work out the cause before you fix it.
That habit, reading the error before searching for it, is worth more than any single fix.

---

### Scene 8 — The notes behind each lesson

The video covers the important parts, but it doesn't read every line aloud.
Each lesson has companion notes in the repository.
They take every command apart piece by piece, explain every line of code, and say when it runs.
They also list the common errors and how to recover from them.
Keep them open while you work.
When the video moves faster than you'd like, the notes are where the detail lives.

---

### Scene 9 — What you need

You need to be comfortable with Python and with a terminal.
You don't need to know Docker or Django's advanced features.
We'll build those up.
Everything in this course uses free tools, and the next lesson checks that your machine has them.
Lessons are short, ten to fifteen minutes, and they build on each other.
Watch them in order, and type the commands yourself rather than just watching.

---

### Scene 10 — Next

In the next lesson, we'll install and verify the toolchain, one tool at a time, and see what to do when a check fails.
