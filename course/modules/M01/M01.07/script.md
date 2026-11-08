# M01.07 — Management commands inside containers

- **Target length:** 12 min
- **Checkpoint at start:** `lesson/M01.07-start` (= `lesson/M01.06-end`)
- **Checkpoint at end:** `lesson/M01.07-end` (adds `projects/telecom/README.md`)
- **Prerequisites:** M1.6; the stack running
- **Working directory:** `projects/telecom/`
- **Labels:** none

## Learning goal
Run Django management commands, shells, tests and logs inside containers; explain `docker compose exec web python manage.py migrate` part by part; tell `exec` from `run`; and explain why restarting a container doesn't apply migrations.

## Script

### Scene 1 — One command, three places

Let's take one command apart: docker compose exec web python manage.py migrate.
> spoken: Let's take one command apart: docker compose exec web python manage dot py migrate.
You run it in a terminal on your own machine, in the project folder with compose.yaml.
> spoken: You run it in a terminal on your own machine, in the project folder with compose dot yaml.
Docker Compose reads that file to find your services.
Exec runs a command inside a container that's already running.
And web is the service we're targeting: our Django app.
Everything after web runs inside that container.
manage.py is Django's command-line entry point, and migrate brings the database schema up to date.
> spoken: Manage dot py is Django's command-line entry point, and migrate brings the database schema up to date.

---

### Scene 2 — Where the tables change

Here's the part that surprises people: the tables don't live in the web container.
Django connects across the Compose network to the db service, Postgres, and that's where the tables change.
> spoken: Django connects across the Compose network to the D B service, Postgres, and that's where the tables change.
It also records each migration it applies, in a table called django_migrations, so running migrate twice is safe.
> spoken: It also records each migration it applies, in a table called Django migrations, so running migrate twice is safe.
The second time, it says: no migrations to apply.

---

### Scene 3 — Restarting doesn't migrate

Let's test a belief many people hold: that restarting the app applies migrations.
Start from a fresh database: down, dash v, then up.
> spoken: Start from a fresh database: down, dash V, then up.
Restart the web container.
Now showmigrations, for the auth app.
Every line shows empty brackets: not applied.
A restart runs the same code again, against the same database.
Migrations happen when you ask for them, usually as an explicit deploy step.
Run migrate, run showmigrations again, and every line has an X.

---

### Scene 4 — A shell inside

You can open Django's interactive shell the same way: docker compose exec web python manage.py shell.
> spoken: You can open Django's interactive shell the same way: docker compose exec web python manage dot py shell.
It's Python, with your settings loaded and your models importable.
For a one-off question, use the dash c flag and pass the code directly.
> spoken: For a one-off question, use the dash C flag and pass the code directly.
How many users exist? Zero, for now.

---

### Scene 5 — An admin user, without typing a password

createsuperuser asks questions interactively, which is fine at a keyboard.
> spoken: Create superuser asks questions interactively, which is fine at a keyboard.
In a script, add the no input flag, and give the password through an environment variable, DJANGO_SUPERUSER_PASSWORD, with exec's dash e flag.
> spoken: In a script, add the no input flag, and give the password through an environment variable, Django superuser password, with exec's dash E flag.
The username and email go on the command line.
Superuser created successfully.
Run the shell one-liner again: one user.
For a real password, don't type it on the command line, where it lands in your shell history: read it from a file or a prompt instead.

---

### Scene 6 — exec versus run

There's a sibling command, run, and it's easy to mix up with exec.
Exec enters the container that's already running, so it shares its state.
Run creates a brand-new container from the same service definition.
Watch: exec web hostname prints one ID.
> spoken: Watch: exec web hostname prints one I D.
Run, with remove and no deps, web hostname prints a different one.
> spoken: Run, with remove and no deps, web hostname prints a different one.
The remove flag deletes the temporary container afterwards.
No deps means: don't start the database just for this.
Use run for one-off tasks when the service isn't up; use exec for everything else.

---

### Scene 7 — Tests, checks, logs

Tests run inside the container too: docker compose exec web pytest.
> spoken: Tests run inside the container too: docker compose exec web pie test.
That matters, because inside the container, tests can reach the real Postgres, by its service name.
Ten passed.
Two quick checks belong in your routine.
manage.py check: system check identified no issues.
> spoken: Manage dot py check: system check identified no issues.
And makemigrations with check and dry run: no changes detected.
> spoken: And make migrations with check and dry run: no changes detected.
That second one catches model changes that someone forgot to turn into a migration.
And when something misbehaves, docker compose logs, with dash f, follows the output.
> spoken: And when something misbehaves, docker compose logs, with dash F, follows the output.
Control C stops following, not the container.

---

### Scene 8 — Writing it down

None of this needed new code, but it needs documentation.
The project README now has a table: each everyday command, where it runs, and what it does.
> spoken: The project read me now has a table: each everyday command, where it runs, and what it does.
And a troubleshooting table, with the errors from this module and their fixes.
The next person to join doesn't have to rediscover any of it.

---

### Scene 9 — Next

So: your terminal runs Compose, Compose reaches into web, and Django changes the database.
But there's still a gap: when Compose starts web, is the database actually ready?
That's the next lesson.
