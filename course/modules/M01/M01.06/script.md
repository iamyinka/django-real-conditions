# M01.06 — Volumes: bind mounts vs. named volumes

- **Target length:** 11 min
- **Checkpoint at start:** `lesson/M01.06-start` (= `lesson/M01.05-end`)
- **Checkpoint at end:** `lesson/M01.06-end`
- **Prerequisites:** M1.5; the stack from M1.5 running
- **Working directory:** `projects/telecom/`
- **Labels:** none

## Learning goal
Say where container data lives, predict what survives `docker compose down` and what `down -v` destroys, persist Postgres data in a named volume at the correct PostgreSQL 18 path, and bind-mount code for live reload.

## Script

### Scene 1 — Where did my data go?

Let's put something in the database and see whether it survives.
I'll create a table with one row, using psql inside the db container.
> spoken: I'll create a table with one row, using P S Q L inside the D B container.
Select it back: one row.
Now docker compose down, and docker compose up again.
Select again: relation does not exist.
The table is gone.
We didn't ask for that, so what happened?

---

### Scene 2 — Containers are disposable

Down removes the containers.
Up creates brand new ones from the same images.
Anything a container wrote to its own writable layer disappears with it.
But Postgres doesn't actually write there.
The Postgres image declares a volume at slash var slash lib slash postgresql.
> spoken: The Postgres image declares a volume at var lib Postgres Q L.
When we don't say otherwise, Docker creates an anonymous volume for it: storage with a random name.
Run docker volume ls.
There it is, a long random ID.
Our data still exists, in that volume.
But the new container got a new anonymous volume, empty, and nobody remembers the old name.
That's an orphaned volume: the data is on the disk, and nothing will ever use it again.

---

### Scene 3 — Named volumes

The fix is to give the volume a name.
In the compose file, under db, add volumes: pgdata, colon, slash var slash lib slash postgresql.
> spoken: In the compose file, under D B, add volumes: P G data, mounted at var lib Postgres Q L.
And at the bottom, a top-level volumes section that declares pgdata.
> spoken: And at the bottom, a top level volumes section that declares P G data.
A named volume is storage that Docker manages and that outlives any container.
Compose prefixes it with the project name, so on disk it's telecom underscore pgdata.
> spoken: Compose prefixes it with the project name, so on disk it's telecom P G data.

---

### Scene 4 — The Postgres eighteen path

The mount path matters, and it changed recently.
Many tutorials mount slash var slash lib slash postgresql slash data.
> spoken: Many tutorials mount var lib Postgres Q L data.
Postgres eighteen images keep data one level deeper, in a folder named after the major version, eighteen slash docker.
> spoken: Postgres eighteen images keep data one level deeper, in a folder named after the major version.
Try the old path with eighteen point six, and the container exits with code one.
The message explains the new layout, and tells you to mount the parent folder instead.
So we mount slash var slash lib slash postgresql, which is exactly the volume the image declares.
> spoken: So we mount var lib Postgres Q L, which is exactly the volume the image declares.
This is why version numbers belong in the compose file: copy a snippet written for an older version, and it can fail like this.

---

### Scene 5 — Prove it survives

Up again, create the table, insert the row.
Down, then up.
Select: one row.
The data survived, because the new container mounted the same named volume.

---

### Scene 6 — And prove it can be destroyed

Now docker compose down, with dash v.
> spoken: Now docker compose down, with dash V.
Dash v removes the project's volumes too.
> spoken: Dash V removes the project's volumes too.
Up, select: relation does not exist.
That's the command to use when you want a clean database in development.
It's also the command that destroys everything, so read it twice before you press enter.
Down without dash v: the data stays.
> spoken: Down without dash V: the data stays.
Down with dash v: the data is gone, and there's no undo.
> spoken: Down with dash V: the data is gone, and there's no undo.

---

### Scene 7 — Bind mounts for code

There's a second kind of mount, and it solves a different problem.
Right now, every code change means rebuilding the image.
Under web, add volumes: dot, colon, slash app.
> spoken: Under web, add volumes: dot, mounted at app.
That's a bind mount: your project folder on the host appears at slash app inside the container.
> spoken: That's a bind mount: your project folder on the host appears at app inside the container.
It's the same files, not a copy.
Edit a file in your editor, and the container sees the change immediately.
Runserver notices, and reloads.

---

### Scene 8 — Why the dependencies survive the mount

A bind mount hides whatever the image had at that path.
So why don't we lose our installed packages?
Because back in lesson three, we put the virtual environment at slash opt slash venv, outside slash app.
> spoken: Because back in lesson three, we put the virtual environment at opt venv, outside app.
The mount replaces the code, and leaves the dependencies alone.
That decision pays off here.

---

### Scene 9 — Live reload, live

Let's see it.
I'll change the URL configuration and save.
The logs show runserver detecting the change and restarting.
No rebuild.
Just remember the limit: change pyproject dot toml, and you still need to rebuild, because dependencies live in the image.
> spoken: Just remember the limit: change pyproject dot toml, and you still need to rebuild, because dependencies live in the image.

---

### Scene 10 — Three kinds of storage

So, three kinds of storage.
The container's writable layer: gone when the container goes.
A named volume: managed by Docker, kept until you delete it, right for databases.
A bind mount: a host folder shared into the container, right for code in development.
Containers aren't durable storage; volumes are.
In the next lesson, we run management commands inside these containers, and see why restarting doesn't migrate.
