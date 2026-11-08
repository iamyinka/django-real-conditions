# M01.09 — Non-root containers, permissions, and secrets in development

- **Target length:** 11 min
- **Checkpoint at start:** `lesson/M01.09-start` (= `lesson/M01.08-end`)
- **Checkpoint at end:** `lesson/M01.09-end`
- **Prerequisites:** M1.8
- **Working directory:** `projects/telecom/`
- **Labels:** none

## Learning goal
Run the web container as an unprivileged user, explain what that protects and what it breaks with bind mounts on Linux, and say exactly where development secrets live, who can read them, and why that isn't production-grade.

## Script

### Scene 1 — Who is running this?

Ask the web container who it is: docker compose exec web id.
> spoken: Ask the web container who it is: docker compose exec web I D.
User ID zero: root.
> spoken: User I D zero: root.
Every process in this container runs as root, including Django, and any code an attacker manages to run through it.

---

### Scene 2 — What root inside a container means

Root inside a container isn't automatically root on your machine.
The container is isolated: it has its own file system and process list.
But isolation is a set of walls, and walls occasionally have holes.
A process running as root inside can install packages, change the app's own code, and write anywhere in the container.
And if a vulnerability lets it out of the container, it leaves as root.
Running as an ordinary user removes most of that, for the cost of a few lines.

---

### Scene 3 — Adding a user

In the Dockerfile, after the code is copied, two build arguments: U I D and G I D, both defaulting to one thousand.
> spoken: In the Dockerfile, after the code is copied, two build arguments: U I D and G I D, both defaulting to one thousand.
Then a RUN line that creates a group called app, and a user called app, with those IDs, no home directory, and no login shell.
> spoken: Then a run line that creates a group called app, and a user called app, with those I Ds, no home directory, and no login shell.
Then USER app.
> spoken: Then user app.
Every instruction after that line, and the running container itself, use this user.
Notice what we didn't do: we didn't hand the code over to the app user.
The code stays owned by root, so the app can read it, but not change it.
Port eight thousand still works, because only ports below one thousand twenty-four need root.

---

### Scene 4 — Prove it

Rebuild, and ask again: user ID one thousand, app.
> spoken: Rebuild, and ask again: user I D one thousand, app.
Try to write to the root folder: permission denied.
Try to write into the virtual environment: permission denied.
Try pip install: permission denied.
And the health check still passes, so the app itself is unaffected.

---

### Scene 5 — A mistake worth showing

While I was preparing this lesson, I made a mistake that teaches the next point better than any slide.
I wanted to prove the code in the image is read-only, so I ran a one-off container with compose run, and tried to append to manage dot py.
> spoken: I wanted to prove the code in the image is read-only, so I ran a one off container with compose run, and tried to append to manage dot py.
It worked.
And the line landed in the real manage dot py on my laptop.
> spoken: And the line landed in the real manage dot py on my laptop.
Compose run uses the service definition, including the bind mount, so slash app wasn't the image's code at all.
> spoken: Compose run uses the service definition, including the bind mount, so app wasn't the image's code at all.
It was my working copy.
I restored the file from Git, and redid the test with plain docker run, with no mount: permission denied, as expected.
The lesson: with a bind mount, the container is writing to your files.

---

### Scene 6 — Bind mounts and user IDs on Linux

That leads to the real cost of a non-root user.
When the container creates a file in a bind mount, say a new migration, the file is owned by user one thousand on your host.
On macOS and Windows, Docker Desktop translates ownership, so you won't notice.
On Linux, there's no translation.
If your own user ID isn't one thousand, those files belong to someone else, and you can't edit them without sudo.
> spoken: If your own user I D isn't one thousand, those files belong to someone else, and you can't edit them without soo doo.
That's why U I D and G I D are build arguments.
On Linux, build with your own IDs, and the container's user matches yours.
> spoken: On Linux, build with your own I Ds, and the container's user matches yours.

---

### Scene 7 — Where secrets live in development

Now secrets.
Our development secrets live in dot env, in the project folder.
> spoken: Our development secrets live in dot env, in the project folder.
Git ignores it: there are zero tracked dot env files.
> spoken: Git ignores it: there are zero tracked dot env files.
Docker ignores it: list slash app in the image, and it isn't there.
> spoken: Docker ignores it: list the app folder in the image, and it isn't there.
And the image history mentions none of the values.
The values reach the container only when it starts, through env file in compose.
> spoken: The values reach the container only when it starts, through env file in compose.
The secret scanner runs on every commit, and again in CI.
> spoken: The secret scanner runs on every commit, and again in C I.

---

### Scene 8 — The limits of dot env

Be honest about what this does and doesn't protect.
> spoken: Be honest about what this does and doesn't protect.
Environment variables are visible to anyone who can run docker inspect, or exec into the container and print the environment.
Crash reports and debug pages can include them too.
On a laptop, with throwaway values, that's acceptable.
In production, secrets come from a secret store, are scoped to the services that need them, and can be rotated without a rebuild.
That's Module seven.
For now, the rule is simple: development values are throwaway, and they never get reused anywhere real.

---

### Scene 9 — Module one, done

That completes the skeleton.
Django six point one and Postgres eighteen, in containers, with configuration from the environment, persistent data, health checks, and a non-root user.
Next, we ship it the professional way: one issue, one branch, one pull request, reviewed, and squash merged.
