# M01.08 — Health checks, readiness, and startup order

- **Target length:** 12 min
- **Checkpoint at start:** `lesson/M01.08-start` (= `lesson/M01.07-end`)
- **Checkpoint at end:** `lesson/M01.08-end`
- **Prerequisites:** M1.7
- **Working directory:** `projects/telecom/`
- **Labels:** none

## Learning goal
Close the gap between "started" and "ready": add liveness and readiness endpoints, a bounded `wait_for_db` command, and Compose health checks with `depends_on: condition: service_healthy`, then prove each one by stopping the database.

## Script

### Scene 1 — Started isn't ready

Remember the comment in our compose file: depends on db is about start order only.
> spoken: Remember the comment in our compose file: depends on D B is about start order only.
Compose starts the db container, then immediately starts web.
> spoken: Compose starts the D B container, then immediately starts web.
But a started Postgres container still needs a few seconds before it accepts connections, longer on the very first run, when it creates the database.
If Django tries to connect in that window, it fails.
And if the database goes away later, how would anything notice?
We need to ask two questions, often, and automatically.

---

### Scene 2 — Two questions

The first question is liveness: is the process alive and able to answer at all?
The second is readiness: can this instance do useful work right now?
They sound alike, but they lead to different actions.
If a process isn't alive, restart it.
If it's alive but not ready, stop sending it traffic, and wait.
Restarting a web server never fixes a broken database.

---

### Scene 3 — A core app with two probes

We'll add a small app called core, for project-wide plumbing.
Its views file has two functions.
healthz returns a JSON status of OK, and deliberately touches nothing else.
> spoken: Health Z returns a Jason status of OK, and deliberately touches nothing else.
readyz opens a database cursor and runs select one.
> spoken: Ready Z opens a database cursor and runs select one.
If that works, it returns OK.
If the database raises an error, it logs the full details, and returns status five oh three: service unavailable.
The response says only which check failed, never the error text, because probe URLs are often reachable by people who shouldn't see connection details.
Both are marked never cache, since a cached OK from five minutes ago is worse than no answer, and both accept GET only.

---

### Scene 4 — Failing fast

One small settings change goes with this.
Under database options, connect timeout, five seconds.
> spoken: Under database options, connect timeout, five seconds.
Without it, connecting to an unreachable host can hang for minutes, and so would readyz, and every request.
> spoken: Without it, connecting to an unreachable host can hang for minutes, and so would ready Z, and every request.

---

### Scene 5 — Waiting, with a limit

Next, a management command: wait for db.
> spoken: Next, a management command: wait for D B.
It tries to connect, and if that fails, it sleeps and tries again.
But only until a deadline: thirty seconds by default.
Then it gives up with an error, and a non-zero exit code.
That limit is the important part.
Retrying forever turns an outage into a container that hangs silently, and nobody gets told.
It measures time with a monotonic clock, so a system clock change can't stretch or shrink the wait.

---

### Scene 6 — Compose health checks

Now teach Compose to ask the questions.
The db service gets a health check that runs pg_isready every five seconds.
> spoken: The D B service gets a health check that runs P G is ready every five seconds.
Notice the dash h, one two seven point zero point zero point one.
> spoken: Notice the dash H, one two seven point oh point oh point one.
That forces a network connection, and there's a reason, which we'll prove in a minute.
Web's depends on becomes: db, condition, service healthy.
> spoken: Web's depends on becomes: D B, condition, service healthy.
Compose now waits until db reports healthy before starting web.
> spoken: Compose now waits until D B reports healthy before starting web.
Web gets its own health check, which fetches healthz with Python's standard library, because the slim image has no curl.
> spoken: Web gets its own health check, which fetches health Z with Python's standard library, because the slim image has no curl.
It checks liveness, not readiness: if web's health depended on the database, a database outage would mark web unhealthy too, and hide where the problem really is.
Start period and start interval give the app time to boot, while probing often enough that healthy shows up quickly.
And web's command now runs wait for db first, then runserver.
> spoken: And web's command now runs wait for D B first, then runserver.

---

### Scene 7 — Watch it start

Down, dash v, and up, from scratch.
> spoken: Down, dash V, and up, from scratch.
db: waiting.
> spoken: D B: waiting.
db: healthy.
> spoken: D B: healthy.
Only then: web, starting.
The web logs say: database available, attempt one.
A few seconds later, docker compose ps shows both containers healthy.

---

### Scene 8 — Break the database

Now stop the database, and ask both probes.
Healthz: two hundred, OK.
> spoken: Health Z: two hundred, O K.
Readyz: five oh three, unavailable.
> spoken: Ready Z: five oh three, unavailable.
Exactly the split we wanted.
The web log shows why: failed to resolve host db.
> spoken: The web log shows why: failed to resolve host D B.
Not connection refused: a stopped service disappears from DNS completely.
> spoken: Not connection refused: a stopped service disappears from D N S completely.
Run wait for db with a three-second timeout: three attempts, then database still unavailable, exit code one.
> spoken: Run wait for D B with a three second timeout: three attempts, then database still unavailable, exit code one.
Start the database again, and wait for db succeeds on its first try. Readyz is back to two hundred.
> spoken: Start the database again, and wait for D B succeeds on its first try. Ready Z is back to two hundred.

---

### Scene 9 — Why the health check uses TCP

Back to that dash h.
> spoken: Back to that dash H.
I polled a brand-new Postgres container every fraction of a second, checking readiness two ways: over the local socket, and over the network.
At one point, the socket check said ready, while the network check said down.
That's the image's first-run setup: it starts a temporary server, listening only on the socket, creates the database, then restarts.
A socket-based health check can report healthy in that window, just before the server goes away.
Checking over the network avoids it.

---

### Scene 10 — Tests

Each piece has a test.
Healthz returns OK without touching the database; pytest django fails the test if it tries.
> spoken: Health Z returns OK without touching the database; pie test Django fails the test if it tries.
Readyz returns OK against the real Postgres.
> spoken: Ready Z returns OK against the real Postgres.
Readyz returns five oh three when the database raises, and the password in the error message never reaches the response.
> spoken: Ready Z returns five oh three when the database raises, and the password in the error message never reaches the response.
And wait for db: it succeeds after two failures, and it gives up at the deadline, using a fake clock so the test takes no time.
> spoken: And wait for D B: it succeeds after two failures, and it gives up at the deadline, using a fake clock so the test takes no time.
Sixteen passed.

---

### Scene 11 — Next

One problem left in this container: it runs as root.
Next lesson, we fix that, and look at how secrets reach the container.
