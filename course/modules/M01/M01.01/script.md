# M01.01 — The telecom field-service problem

- **Target length:** 10 min
- **Checkpoint at start:** `lesson/M00.04-end`
- **Checkpoint at end:** `lesson/M01.01-end` (no code; the first issue exists on GitHub)
- **Prerequisites:** Module 0
- **Working directory:** the repository root
- **Labels:** Simulated (carrier provisioning, outage detection and the SMS gateway are simulated throughout Project 1)

## Learning goal
Describe Project 1's users, workflows and MVP boundary, say which parts are simulated and why, and turn the first slice of work into an issue with acceptance criteria you can check.

## Script

### Scene 1 — A Tuesday morning outage

It's a Tuesday morning, and a fiber cut has taken out internet for a neighborhood.
Two hundred customers notice at once.
Some call, some use the website, and some try both, twice.
A dispatcher needs to send the right technician to the right street box.
That technician will spend the next hour in a basement with no signal.
And every customer wants to know: is anyone working on this?
That's the business our first project serves.

---

### Scene 2 — The people

Five kinds of people use this app.
Customers report problems and want updates.
Support staff take reports by phone and fix bad data.
Dispatchers decide which technician goes where.
Field technicians do the work, often offline.
And administrators manage accounts and settings.
Each group needs different screens, and different permissions, which is Module three.

---

### Scene 3 — The workflows

Here's the core flow.
A customer has a service site, like a house or an office, with a subscription to a plan.
When something breaks, someone reports it, and the report becomes a ticket.
The ticket moves through fixed states: reported, triaged, assigned, en route, on site, resolved, and closed.
A dispatcher assigns a technician.
The technician records notes and photos on site, even with no connection, and the changes sync when the signal comes back.
Customers get updates by text message and email.
And managers get reports: how long tickets stay open, and how long assignment and repair take.

---

### Scene 4 — Where it hurts

Each step hides a real problem.
Reports arrive twice, so we need to recognize a duplicate.
Two dispatchers can assign the same technician at the same second, so we need to handle races.
Technicians work offline, so changes must queue on the device and sync without silently losing anything.
Text messages cost money and trust, so each update must go out once, not zero times and not three.
These problems are what Modules two to seven are really about.

---

### Scene 5 — Drawing the MVP line

We can't build a whole telecom company.
So we draw a line, and we call what's inside it the MVP: the minimum viable product.
> spoken: So we draw a line, and we call what's inside it the M V P: the minimum viable product.
Inside: customers, sites, subscriptions, tickets and their states, dispatch, offline field updates with photos, notifications, audit history, and reports.
Outside, for later: route optimization, a native phone app, billing, and real network monitoring.
Writing down what's out is just as important as what's in.
It's how you say no to scope creep politely.

---

### Scene 6 — What's simulated, and why

Three parts of this system would normally belong to someone else.
Turning service on at the carrier, detecting outages from network equipment, and sending text messages through a provider.
We'll build stand-ins for all three, and label them simulated every time they appear.
A real SMS provider costs money, needs an account, and can't fail on command.
> spoken: A real S M S provider costs money, needs an account, and can't fail on command.
Our fake one can time out, deliver twice, or report failure whenever a lesson needs it.
That's more useful for learning than the real thing, as long as nobody mistakes it for the real thing.

---

### Scene 7 — Success you can measure

How will we know the app works under pressure?
We write the targets down now, as hypotheses, and test them later.
A hundred identical submissions at once must create exactly one ticket.
Two competing assignments must produce one winner and one clear error.
Fifty queued offline changes must all arrive, or show up as explicit conflicts, with none silently lost.
Until a test has run, these are expectations, not facts.

---

### Scene 8 — The first issue

The first slice of work is small: an empty Django project running in containers, with a database.
Let's write it as an issue.
The title says what: a runnable skeleton in Docker Compose.
The body says why: everything else builds on it.
Then the scope, one line per lesson in this module.
Then what's out of scope: production settings, CI, and any business models.
> spoken: Then what's out of scope: production settings, C I, and any business models.
And acceptance criteria that anyone can check with a command.
The containers start with one command.
The health endpoint answers.
The tests pass inside the container.
That issue is our contract for the rest of the module.

---

### Scene 9 — Next

Next lesson, we start from an empty folder: a new Django project, settings split by environment, and configuration read from environment variables.
