# M01.04 — Build context, .dockerignore, locking, and caching

- **Target length:** 12 min
- **Checkpoint at start:** `lesson/M01.04-start` (= `lesson/M01.03-end`)
- **Checkpoint at end:** `lesson/M01.04-end`
- **Prerequisites:** M1.3
- **Working directory:** `projects/telecom/`
- **Labels:** Simulated (the secret in scene 3 is a fake value)

## Learning goal
Shrink the build context with `.dockerignore`, keep secrets out of image layers, and order the Dockerfile so a code change rebuilds in seconds instead of reinstalling every dependency.

## Script

### Scene 1 — Two problems, one cause

Last lesson ended with two problems.
The image contains my Mac's virtual environment, which is useless in Linux.
And changing one line of Python makes the build reinstall every package.
Both come from the same line: COPY dot dot.
> spoken: Both come from the same line: copy dot dot.

---

### Scene 2 — What the builder receives

When you run docker build, the first thing that happens is the context transfer.
The docker command packs up the folder you named and sends it to the builder.
Watch the output: transferring context, six hundred and sixty-three kilobytes.
Our actual source code is a small fraction of that.
The rest is the virtual environment, caches, and anything else lying around.
Every one of those files gets sent on every build, and COPY dot dot puts all of them in the image.
> spoken: Every one of those files gets sent on every build, and copy dot dot puts all of them in the image.

---

### Scene 3 — The dangerous part

Size is the annoying part.
Secrets are the dangerous part.
I'll create a dot env file with a fake database password, like the one we'll use in lesson five.
> spoken: I'll create a dot env file with a fake database password, like the one we'll use in lesson five.
Build, then run cat on slash app slash dot env inside the image.
> spoken: Build, then run cat on the dot env file inside the image.
There's the password, baked into a layer.
Anyone who can pull this image can read it.
And deleting the file in a later instruction doesn't help: the earlier layer still contains it.

---

### Scene 4 — dot dockerignore

The fix is a file called dot dockerignore, next to the Dockerfile.
> spoken: The fix is a file called dot docker ignore, next to the Dockerfile.
It uses patterns like dot gitignore, but it controls a different thing: what leaves your machine and reaches the builder.
> spoken: It uses patterns like dot git ignore, but it controls a different thing: what leaves your machine and reaches the builder.
We exclude the virtual environment and Python caches.
We exclude every dot env file, except dot env dot example, which holds placeholders only.
> spoken: We exclude every dot env file, except dot env dot example, which holds placeholders only.
Local databases and media, the Git folder, test caches.
And the Dockerfile and compose files themselves, so editing them doesn't invalidate the code layer.
Rebuild, and the context is one point three seven kilobytes.
And the dot env file? No such file.
> spoken: And the dot env file? No such file.

---

### Scene 5 — How the cache decides

Now the slow rebuilds.
Docker caches each layer, and reuses it if the instruction is the same and the files it copied are the same.
But once one layer changes, every layer after it is rebuilt.
In our Dockerfile, COPY dot dot comes before uv sync.
> spoken: In our Dockerfile, copy dot dot comes before U V sync.
Change any file, and the copy layer changes, so the install layer below it runs again.
Here's the proof: I add one comment to the URL file and rebuild.
Installed nine packages.
On a slow connection, with a bigger project, that's minutes, on every edit.

---

### Scene 6 — Dependencies first, code last

The fix is to order layers from least likely to change, to most likely.
First copy only pyproject dot toml and uv dot lock.
> spoken: First copy only pyproject dot toml and U V dot lock.
Then install dependencies from them.
Then copy the code.
Now, editing Python changes only the last layer.
The install step's inputs, the two dependency files, haven't changed, so Docker reuses it.

---

### Scene 7 — The install line, piece by piece

The install line gets more interesting.
RUN, with a mount flag, type cache, target slash root slash dot cache slash uv.
> spoken: Run, with a mount flag of type cache, targeting U V's cache folder.
That gives uv a download cache that survives between builds, but isn't stored in the image.
> spoken: That gives U V a download cache that survives between builds, but isn't stored in the image.
Then uv sync, with the locked flag, and the no install project flag.
> spoken: Then U V sync, with the dash dash locked flag, and the dash dash no install project flag.
Locked still means: install exactly what the lock file says, or fail.
No install project means: install the dependencies only, because our code isn't in the image yet.
Two more environment variables support this.
UV_COMPILE_BYTECODE precompiles the dependencies once, at build time, so containers start faster.
> spoken: U V compile bytecode precompiles the dependencies once, at build time, so containers start faster.
And UV_LINK_MODE equals copy, because the cache is a separate mount, and uv can't hard-link files across it.
> spoken: And U V link mode equals copy, because the cache is a separate mount, and U V can't hard link files across it.

---

### Scene 8 — Proof

Build once to fill the cache.
Then change one line of Python, and build again.
The dependency layer says CACHED.
> spoken: The dependency layer says cached.
Only the final copy runs, and it takes a fraction of a second.
The image also shrank, from three hundred and eighty-five megabytes to three hundred and forty-one, because the Mac virtual environment is gone.

---

### Scene 9 — What the lock file buys you

One last point about locking.
pyproject dot toml says what we want.
> spoken: Pyproject dot toml says what we want.
uv dot lock records what we got: every package, its exact version, and a hash of the file.
> spoken: U V dot lock records what we got: every package, its exact version, and a hash of the file.
Build this image next month, on another machine, and you get the same packages.
If someone edits pyproject dot toml and forgets to update the lock, the locked flag stops the build with a clear error, instead of letting versions drift silently.
> spoken: If someone edits pyproject dot toml and forgets to update the lock, the locked flag stops the build with a clear error, instead of letting versions drift silently.

---

### Scene 10 — Next

The image is small, safe, and fast to rebuild.
Next, we add a real database, and run both containers together with Compose.
