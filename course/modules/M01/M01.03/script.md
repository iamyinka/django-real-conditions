# M01.03 — Images, containers, and layers: the Dockerfile

- **Target length:** 14 min
- **Checkpoint at start:** `lesson/M01.03-start` (= `lesson/M01.02-end`)
- **Checkpoint at end:** `lesson/M01.03-end`
- **Prerequisites:** M1.2; Docker running (`sh scripts/doctor.sh`)
- **Working directory:** `projects/telecom/`
- **Labels:** none

## Learning goal
Write a Dockerfile for the Django project and explain each instruction, the difference between an image and a container, what a layer is, and where the build runs compared with where the container runs.

## Script

### Scene 1 — "It works on my machine"

Our project runs, on this laptop, with this Python, and the packages in this virtual environment.
A teammate on Linux, or a server next year, has none of that.
A container image packages the operating system files, Python, our dependencies, and our code into one artifact.
Anyone with Docker can run it and get the same environment.

---

### Scene 2 — Image versus container

Two words get mixed up constantly, so let's pin them down.
An image is a read-only template: a stack of file system snapshots plus some settings, like which command to run.
A container is a running instance of an image, with its own thin, writable layer on top.
The usual analogy is a class and an object.
One image, many containers, each with its own state.
Where the analogy breaks: when a container is deleted, everything it wrote into that writable layer goes with it.
That's why databases need volumes, which is lesson six.

---

### Scene 3 — The base image

Create a file called Dockerfile, with no extension, in the telecom folder.
Line one: a syntax comment that tells Docker which Dockerfile parser to use.
Then FROM: python, three point fourteen point ten, slim trixie.
> spoken: Then from: Python, three point fourteen point ten, slim trixie.
That's the official Python image, on Debian thirteen, codenamed trixie.
Slim means compilers and documentation are left out, so the image is smaller.
We pin the exact patch version, so every build starts from the same Python.
A tag like python three, with nothing more specific, would quietly change under you.

---

### Scene 4 — Bringing in uv

Next: COPY, from the uv image, the uv binaries into slash bin.
> spoken: Next: copy, from the U V image, the U V binaries into slash bin.
COPY with a from flag copies files out of another image, without installing anything.
> spoken: Copy with a from flag copies files out of another image, without installing anything.
It's faster and more predictable than installing uv with pip, and the version is pinned in the tag.
> spoken: It's faster and more predictable than installing U V with pip, and the version is pinned in the tag.

---

### Scene 5 — Environment settings

Then a block of ENV lines.
> spoken: Then a block of env lines.
PYTHONDONTWRITEBYTECODE stops Python writing cache files next to the code at runtime.
> spoken: Python don't write bytecode stops Python writing cache files next to the code at runtime.
PYTHONUNBUFFERED makes print statements and logs appear immediately, so docker logs shows them in real time.
> spoken: Python unbuffered makes print statements and logs appear immediately, so docker logs shows them in real time.
UV_PROJECT_ENVIRONMENT tells uv to build the virtual environment at slash opt slash venv, outside the code folder.
> spoken: U V project environment tells U V to build the virtual environment at opt venv, outside the code folder.
Remember that; it pays off in lesson six.
And PATH puts that environment first, so plain python means the right Python.
> spoken: And path puts that environment first, so plain Python means the right Python.

---

### Scene 6 — Code, dependencies, command

WORKDIR slash app sets the working directory for everything that follows, and creates it.
> spoken: Workdir app sets the working directory for everything that follows, and creates it.
COPY dot dot copies the build context, our project folder, into slash app.
> spoken: Copy dot dot copies the build context, our project folder, into app.
RUN uv sync, with the locked flag, installs exactly what uv dot lock says.
> spoken: Run U V sync, with the locked flag, installs exactly what U V dot lock says.
If the lock file doesn't match pyproject dot toml, the build fails instead of quietly resolving new versions.
> spoken: If the lock file doesn't match pyproject dot toml, the build fails instead of quietly resolving new versions.
EXPOSE eight thousand is documentation only: it says which port the app listens on, and publishes nothing.
> spoken: Expose eight thousand is documentation only: it says which port the app listens on, and publishes nothing.
And CMD is the default command when a container starts: runserver, on zero point zero point zero point zero, port eight thousand.
> spoken: And C M D is the default command when a container starts: runserver, on zero point zero point zero point zero, port eight thousand.

---

### Scene 7 — Layers

Each instruction that changes files creates a layer: a snapshot of what changed.
Layers are stacked, and Docker reuses a layer from cache if the instruction, and everything before it, is unchanged.
Run docker history on the image, and you can see each layer and its size.
The copy of our project is fifty-one megabytes.
Our code is a few kilobytes.
Hold that thought; it's the whole of the next lesson.

---

### Scene 8 — Where the build runs

Build it with docker build, dash t telecom, dot.
> spoken: Build it with docker build, dash T telecom, dot.
Dash t gives the image a name.
> spoken: Dash T gives the image a name.
The final dot is the build context: the folder whose files are sent to the builder.
That's the "where" of this lesson.
The docker command runs on your machine, but the build happens inside the Docker daemon, which on a Mac is a Linux virtual machine.
The builder can only see files in the context you sent it.
It can't reach into your home folder, and a path outside the context simply doesn't exist for it.

---

### Scene 9 — Run it

Now run a container from it.
docker run, remove flag, dash p one two seven point zero point zero point one colon eight thousand and one colon eight thousand, dash e with the secret key, and the image name.
> spoken: Docker run, dash dash R M, then dash P, one two seven point oh point oh point one, port eight thousand and one, to port eight thousand, then dash E with the secret key, and the image name.
Dash p publishes the port: connections to port eight thousand and one on your machine go to port eight thousand in the container.
> spoken: Dash P publishes the port: connections to port eight thousand and one on your machine go to port eight thousand in the container.
Binding it to one two seven point zero point zero point one keeps it off your local network.
> spoken: Binding it to one two seven point oh point oh point one keeps it off your local network.
Dash e sets an environment variable inside the container, because the image doesn't contain the secret, and shouldn't.
> spoken: Dash E sets an environment variable inside the container, because the image doesn't contain the secret, and shouldn't.
Open localhost, port eight thousand and one, and there's the welcome page, served from Linux, by Python three fourteen point ten.

---

### Scene 10 — Why zero point zero point zero point zero

Let's break it on purpose.
I'll run the same image, but tell runserver to listen on one two seven point zero point zero point one, inside the container.
> spoken: I'll run the same image, but tell runserver to listen on one two seven point oh point oh point one, inside the container.
The browser gets an empty reply.
Inside a container, one two seven point zero point zero point one is the container itself.
> spoken: Inside a container, one two seven point oh point oh point one is the container itself.
Docker forwards your connection into the container's network interface, and nothing is listening there.
Zero point zero point zero point zero means: listen on every interface, including the one Docker forwards to.
Publishing on the host side to one two seven point zero point zero point one is what keeps it private.
> spoken: Publishing on the host side to one two seven point oh point oh point one is what keeps it private.
Two different addresses, in two different places.

---

### Scene 11 — Something's off

One more look before we move on.
Open a shell in the image and list slash app.
> spoken: Open a shell in the image and list the app folder.
There's a dot venv folder in here: the virtual environment from my Mac, forty-nine megabytes and over four thousand files.
> spoken: There's a dot V env folder in here: the virtual environment from my Mac, forty nine megabytes and over four thousand files.
It's useless in Linux, and it's in the image because COPY dot dot copied everything.
> spoken: It's useless in Linux, and it's in the image because copy dot dot copied everything.
And if I change one line of Python and rebuild, uv sync runs again and reinstalls every package.
> spoken: And if I change one line of Python and rebuild, U V sync runs again and reinstalls every package.
Both problems have the same cause, and the next lesson fixes them.
