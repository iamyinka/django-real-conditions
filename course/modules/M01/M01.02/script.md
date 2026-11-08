# M01.02 — Starting from nothing

- **Target length:** 12 min
- **Checkpoint at start:** `lesson/M01.02-start` (empty `projects/telecom/`)
- **Checkpoint at end:** `lesson/M01.02-end`
- **Prerequisites:** M0.2 (uv and Python 3.14 verified)
- **Working directory:** `projects/telecom/`
- **Labels:** none

## Learning goal
Create a Django 6.1 project with uv, split settings into base, dev and test, read secrets and per-environment values from environment variables, and explain what `manage.py` does when you run a command.

## Script

### Scene 1 — An empty folder

We start in an empty folder: projects slash telecom.
> spoken: We start in an empty folder: projects, telecom.
By the end of this lesson, it'll hold a Django project that refuses to start without its secret key.
That refusal is a feature, and you'll see why.

---

### Scene 2 — A project file with uv

First, a project file.
Run uv init, with the bare flag, the python flag set to three fourteen, and the name telecom.
> spoken: Run U V init, with the dash dash bare flag, the python flag set to three fourteen, and the name telecom.
Bare means: create only pyproject dot toml, with no sample code.
> spoken: Bare means: create only pyproject dot toml, with no sample code.
That file is the project's identity card: its name, the Python versions it supports, and its dependencies.
Now add Django, pinned to an exact version: uv add django, two equals signs, six point one point three.
> spoken: Now add Django, pinned to an exact version: U V add Django, at exactly six point one point three.
uv does three things here.
> spoken: U V does three things here.
It records the dependency in pyproject dot toml.
> spoken: It records the dependency in pyproject dot toml.
It writes uv dot lock, with the exact version and checksum of every package, including Django's own dependencies.
> spoken: It writes U V dot lock, with the exact version and checksum of every package, including Django's own dependencies.
And it creates a virtual environment, dot venv, and installs everything into it.
> spoken: And it creates a virtual environment, dot V env, and installs everything into it.
The lock file gets committed; the virtual environment never does.

---

### Scene 3 — startproject

Now create the Django project.
uv run django-admin startproject config, then a space and a dot.
> spoken: U V run Django admin startproject config, then a space and a dot.
uv run means: run this command inside the project's virtual environment, without activating anything.
> spoken: U V run means: run this command inside the project's virtual environment, without activating anything.
Config is the name of the settings package.
The dot at the end means "put it here", instead of in an extra nested folder.
We get manage dot py, and a config folder with settings, URLs, and the entry points for web servers.
> spoken: We get manage dot py, and a config folder with settings, U R Ls, and the entry points for web servers.

---

### Scene 4 — What manage.py actually does

Open manage dot py.
> spoken: Open manage dot py.
It's short.
It sets one environment variable, DJANGO_SETTINGS_MODULE, which tells Django which settings file to load.
> spoken: It sets one environment variable, Django settings module, which tells Django which settings file to load.
It uses setdefault, so if that variable is already set, your value wins.
> spoken: It uses set default, so if that variable is already set, your value wins.
Then it hands the command line to Django, which finds the command, like runserver or migrate, and runs it.
Every management command starts here, and every one loads the settings first.
So a mistake in settings breaks every command at once.

---

### Scene 5 — Why one settings file isn't enough

The generated settings file has a problem.
It contains a secret key, written right there in the code.
That key signs sessions and password reset links.
Commit it to a public repository, and anyone can forge them.
It also has debug turned on, which is fine on a laptop and dangerous on a server.
Development, tests, and production need different values.
So we split the settings.

---

### Scene 6 — A settings package

The single settings file becomes a folder: base, dev, and test.
Base holds what every environment shares.
Dev and test each import everything from base, then override only what differs.
Dev turns debug on by default and allows only localhost.
Test uses a fast password hasher, because the real one is slow on purpose, and in tests that slowness is pure cost.
manage dot py now points to dev by default, and the test runner is configured to use test.
> spoken: Manage dot py now points to dev by default, and the test runner is configured to use test.
And the hard-coded secret key is gone.

---

### Scene 7 — Reading the environment

Instead, values come from environment variables, through three small helpers in config slash env dot py.
> spoken: Instead, values come from environment variables, through three small helpers in config, env dot py.
We could use a library, but the whole thing fits on one screen, and you can see exactly what happens.
env reads a string.
If the variable is missing or empty, and there's no default, it raises an error that names the variable.
env bool reads true or false, and it rejects anything else.
That matters more than it looks.
Imagine someone types t, u, r, e.
A lazy parser would quietly treat that as false, and switch off whatever setting it controls.
Ours stops and says so.
env list splits a comma-separated value and drops the blanks.

---

### Scene 8 — When does this run?

Here's the timing that makes this work.
Settings are Python modules, and their code runs when they're imported: at startup, before the first request.
So a missing secret doesn't cause an error at three in the morning when someone logs in.
It stops the process immediately, with a message that says what to fix.
Failing early and loudly is the goal.

---

### Scene 9 — Watch it fail, then run

Let's try it.
Run uv run python manage dot py check, with no secret key set.
> spoken: Run U V run python manage dot py check, with no secret key set.
Improperly configured: set the DJANGO_SECRET_KEY environment variable.
> spoken: Improperly configured: set the Django secret key environment variable.
Now the typo case: a key, and debug set to t, u, r, e.
Debug must be true or false, got ture.
> spoken: Debug must be true or false, got T U R E.
And with a valid key: system check identified no issues.
Start the development server with runserver, open localhost port eight thousand, and there's Django's welcome page.
For now, the database is SQLite, a single file; Postgres arrives with Compose in lesson five.
> spoken: For now, the database is S Q Lite, a single file; Postgres arrives with Compose in lesson five.

---

### Scene 10 — Tests for the helpers

These helpers decide whether the app starts at all, so they get tests.
Missing values, empty values, the accepted true and false spellings, the typo, and list splitting.
Run uv run pytest.
> spoken: Run U V run pytest.
Ten passed.

---

### Scene 11 — Next

The project runs, but only on this machine, with this Python.
Next lesson, we put it in a container image, line by line.
