# M00.02 — Your toolchain, verified

- **Target length:** 12 min
- **Checkpoint at start:** `lesson/M00.01-end`
- **Checkpoint at end:** `lesson/M00.02-end` (adds `scripts/doctor.sh`)
- **Prerequisites:** a terminal; administrator rights to install software
- **Working directory:** the course repository root
- **Labels:** none

## Learning goal
Install Git, uv, Python 3.14 and Docker with Compose; verify each one, including the Docker daemon itself; and know the first move when a check fails on macOS, Linux, or Windows with WSL2.

## Script

### Scene 1 — Why verify

Before we write any Django, let's make sure your machine is ready.
Installing a tool and verifying it are two different steps.
A command can exist and still not work, and you want to find that out now, not halfway through Module 1.
So for every tool, we'll install it, run a check, and know what a failure looks like.

---

### Scene 2 — The four tools

You need four things.
Git, to track your code and follow the checkpoints.
uv, which installs Python and manages project dependencies.
> spoken: U V, which installs Python and manages project dependencies.
Docker, which runs the apps and their databases in containers.
And Compose, which runs several containers together from one file.
You'll also want a code editor.
I'm using VS Code, but any editor that understands Python is fine.
> spoken: I'm using V S Code, but any editor that understands Python is fine.

---

### Scene 3 — Git

Start with Git.
Run git --version.
> spoken: Run git dash dash version.
Anything from version two point forty upward is fine.
Git also needs to know who you are, because your name and email go into every commit.
Set them once with git config, using the --global flag so they apply to every repository on this machine.
> spoken: Set them once with git config, using the dash dash global flag so they apply to every repository on this machine.
If you'll push to a public repository, use the private no-reply email that GitHub gives you, so your real address isn't published in the history.

---

### Scene 4 — uv and Python

Next, uv.
> spoken: Next, U V.
The install page gives you a one-line command that downloads an installer script and runs it.
Piping a download straight into your shell means you're trusting that server completely.
> spoken: Piping a download straight into your shell means you're trusting that server completely.
If that makes you uneasy, good: download the script first, read it, then run it, or use your package manager instead.
Check it with uv --version.
> spoken: Check it with U V dash dash version.
Now ask uv for Python three fourteen.
> spoken: Now ask U V for Python three fourteen.
It downloads a standalone Python and keeps it separate from anything your operating system uses.
Here's the important part about where Python runs in this course.
The apps run on the Python inside their container images, not on this one.
The Python on your machine is for tools: running checks, formatting code, and helping your editor.

---

### Scene 5 — Docker has two halves

Now Docker.
On macOS and Windows, install Docker Desktop.
On Linux, install Docker Engine from Docker's own repository, rather than an old package from your distribution.
Run docker version.
> spoken: Run docker version.
Look closely: the output has two sections, Client and Server.
The client is the docker command you type.
The server is the Docker daemon, a separate background process that actually builds images and runs containers.
On a Mac or on Windows, that daemon lives inside a small Linux virtual machine that Docker Desktop manages for you.
That's why a container on your Mac is running Linux, not macOS.

---

### Scene 6 — A real failure

Here's the failure you're most likely to see.
I've quit Docker Desktop, and I'll run docker version again.
The client section prints fine.
Then: cannot connect to the Docker daemon.
The command exists, so a quick check that the docker command is installed would pass.
But nothing can run, because the server isn't there.
The fix is to start Docker Desktop, or on Linux, start the docker service.
Wait until it reports that it's running, then check again.
Now both halves answer.

---

### Scene 7 — Prove a container runs

A reachable daemon still isn't the whole story.
Run docker run, with the --rm flag, and the image hello-world.
> spoken: Run docker run, with the dash dash R M flag, and the image hello world.
That pulls a tiny image from Docker Hub, starts a container, prints a message, and exits.
The remove flag deletes the stopped container afterwards, so it doesn't pile up.
If this works, your machine can download images and run containers, which is everything Module 1 needs.

---

### Scene 8 — Compose

Compose comes with Docker Desktop, and on Linux it's a plugin you install alongside the engine.
Run docker compose version, with a space between docker and compose.
> spoken: Run docker compose version, with a space between docker and compose.
Older tutorials use docker-compose with a hyphen.
> spoken: Older tutorials use docker hyphen compose, with a hyphen.
That's the retired standalone program.
This course always uses the plugin form.

---

### Scene 9 — Platform notes

A few differences by platform.
On Linux, you may be told to add yourself to the docker group so you don't need sudo.
> spoken: On Linux, you may be told to add yourself to the docker group so you don't need sudo.
Know what that means: anyone in that group can control the daemon, and the daemon runs as root.
It's effectively root access, so only do it on a machine you control.
On Windows, use WSL two, and keep your code inside the Linux filesystem, under your Linux home folder.
> spoken: On Windows, use W S L two, and keep your code inside the Linux filesystem, under your Linux home folder.
If the code lives on the Windows drive, file sharing with containers becomes very slow.
And on every platform, give Docker at least four gigabytes of memory.
Later modules, with browsers and media processing, are happier with eight.

---

### Scene 10 — One command for all of it

You don't have to remember all of these checks.
The repository has a small script that runs them in order.
From the repository root, run sh scripts/doctor.sh.
> spoken: From the repository root, run S H, scripts, doctor dot S H.
It only reads: it runs version commands and one throwaway container, and changes nothing.
Each line is either ok, or a failure with the fix printed underneath.
Fix failures from the top down, because later checks often depend on earlier ones.
Run it again whenever something feels off.
When every line says ok, you're ready.

---

### Scene 11 — Next

Next, we'll look at how the repository is organized: one repository, five independent apps, and the files that must never be committed.
