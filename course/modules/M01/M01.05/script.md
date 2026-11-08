# M01.05 — Compose: Django and PostgreSQL

- **Target length:** 13 min
- **Checkpoint at start:** `lesson/M01.05-start` (= `lesson/M01.04-end`)
- **Checkpoint at end:** `lesson/M01.05-end`
- **Prerequisites:** M1.4; port 8001 free on the host
- **Working directory:** `projects/telecom/`
- **Labels:** none

## Learning goal
Run Django and PostgreSQL together with Compose, explain service-name DNS versus `localhost`, what publishing a port does (and doesn't do), and diagnose a "connection refused" error from its message.

## Script

### Scene 1 — Why a real database now

SQLite is a fine database, but it isn't the one we'll run in production.
Later modules depend on Postgres features: row locking, exclusion constraints, and real query plans.
> spoken: Later modules depend on Postgres features: row locking, exclusion constraints, and real query plans.
Developing on one database and deploying on another means finding differences in production.
So Postgres comes in now, in its own container.
That gives us two containers, and a reason for Compose.

---

### Scene 2 — Compose in one sentence

Compose reads one file, compose dot yaml, that describes several containers and how they connect, and starts them all with one command.
> spoken: Compose reads one file, compose dot yaml, that describes several containers and how they connect, and starts them all with one command.
Each entry under services is a service: a container definition with a name.
We'll have two: web, for Django, and db, for Postgres.
> spoken: We'll have two: web, for Django, and D B, for Postgres.

---

### Scene 3 — The database driver and settings

Django needs a driver to talk to Postgres.
uv add, psycopg with the binary extra, pinned to three point three point eight.
> spoken: U V add psycho P G, with the binary extra, pinned to three point three point eight.
The binary extra ships a compiled client library, so the slim image doesn't need compilers.
In base settings, the database engine becomes Postgres, and every connection detail comes from the environment: name, user, password, host, and port.
> spoken: In base settings, the database engine becomes Postgres, and every connection detail comes from the environment: name, user, password, host, and port.
The host is the interesting one.
Its value will be D, B: the name of the service.
> spoken: Its value will be D B: the name of the service.

---

### Scene 4 — The env file

Those values live in a file called dot env, which is never committed.
> spoken: Those values live in a file called dot env, which is never committed.
What is committed is dot env dot example, with throwaway development values.
> spoken: What is committed is dot env dot example, with throwaway development values.
So the first step for anyone cloning the project is: copy the example to dot env.
> spoken: So the first step for anyone cloning the project is: copy the example to dot env.
One detail about the Postgres image: it reads the database name, user, and password only the first time it starts with an empty data folder.
Changing them later doesn't change an existing database.
That catches people out, and we'll see why it happens in the next lesson.

---

### Scene 5 — compose dot yaml, line by line

Now the compose file.
> spoken: Now the compose file.
Name telecom sets the project name, so containers, networks, and volumes are prefixed with telecom and never collide with other projects.
Service web: build dot, so Compose builds the image from our Dockerfile.
> spoken: Service web: build dot, so Compose builds the image from our Dockerfile.
env file dot env passes every variable in that file into the web container.
> spoken: Env file, dot env, passes every variable in that file into the web container.
Ports: one two seven point zero point zero point one, eight thousand and one, to eight thousand, the same publishing rule as before.
> spoken: Ports: one two seven point oh point oh point one, port eight thousand and one, to eight thousand, the same publishing rule as before.
Depends on db: start the database container first.
> spoken: Depends on D B: start the database container first.
Note the comment: started isn't the same as ready, and lesson eight deals with that gap.
Service db uses the official Postgres image, eighteen point six.
> spoken: Service D B uses the official Postgres image, eighteen point six.
Its environment passes only the three variables Postgres needs, read from dot env with dollar-brace syntax.
> spoken: Its environment passes only the three variables Postgres needs, read from dot env with dollar brace syntax.
The database doesn't need Django's secret key, so it doesn't get it.
And db has no ports section at all.
> spoken: And D B has no ports section at all.

---

### Scene 6 — Up

Run docker compose up, with dash d for detached, and dash dash build.
> spoken: Run docker compose up, with dash D for detached, and dash dash build.
Compose creates a network called telecom underscore default, builds the web image, and starts both containers.
> spoken: Compose creates a network called telecom default, builds the web image, and starts both containers.
docker compose ps shows them running.
> spoken: Docker compose P S shows them running.
Now apply Django's built-in migrations: docker compose exec web python manage dot py migrate.
> spoken: Now apply Django's built-in migrations: docker compose exec web python manage dot py migrate.
Eighteen migrations, each one OK, applied to Postgres in the other container.
And the welcome page loads on port eight thousand and one.

---

### Scene 7 — Service names are hostnames

How did web find db?
> spoken: How did web find D B?
Compose runs a small DNS server on the project network.
> spoken: Compose runs a small D N S server on the project network.
Every service name resolves to that container's address.
Ask from inside web: db resolves to one seven two point twenty-two point zero point two.
> spoken: Ask from inside web: D B resolves to one seven two point twenty two point oh point two.
And localhost resolves to one two seven point zero point zero point one: the web container itself.
> spoken: And localhost resolves to one two seven point oh point oh point one: the web container itself.

---

### Scene 8 — The classic mistake

So here's the mistake almost everyone makes once.
On a laptop, the database is at localhost, so that's what goes in the settings.
Let's run migrate with the host set to localhost.
Connection refused, on one two seven point zero point zero point one, port five four three two.
> spoken: Connection refused, on one two seven point oh point oh point one, port five four three two.
Read the message before searching for it.
It names the address it tried, and that address is the web container's own loopback.
There's no Postgres inside the web container, so nothing is listening there.
The fix is the service name, D, B.
> spoken: The fix is the service name, D B.

---

### Scene 9 — What a published port means

Now the database's missing ports section.
Publishing a port opens a door from your host into a container.
Web has one, so your browser can reach it.
Db doesn't, so the only way to reach Postgres is from another container on the same network.
> spoken: D B doesn't, so the only way to reach Postgres is from another container on the same network.
That's deliberate: fewer doors, fewer surprises.
And here's a surprise from my own machine.
I have Postgres dot app installed, and it listens on port five four three two on my Mac.
> spoken: I have Postgres dot app installed, and it listens on port five four three two on my Mac.
If I connect a database tool to localhost, port five four three two, it connects happily, to the wrong database.
No error, just different data.
When data looks wrong, check which server you're actually connected to.

---

### Scene 10 — Port conflicts

One more error you'll meet.
If something else already uses host port eight thousand and one, up fails with: bind failed, port is already allocated.
docker ps shows who has it.
> spoken: Docker P S shows who has it.
Stop that container, or pick another host port.
The container port, eight thousand, never needs to change.

---

### Scene 11 — Next

Our database is running, but where is its data actually stored, and what happens when we run docker compose down?
That's the next lesson.
