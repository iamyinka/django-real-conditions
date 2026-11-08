# Exercise — M01.04 Build context, .dockerignore, locking, and caching

**Start from:** `git switch --detach lesson/M01.04-end`, then `git switch -c exercise/m1.4`

## Task
The team is adding `httpx` for calling the (simulated) SMS provider later. Add it, and prove the cache behaves the way the lesson says, in both directions.

## Acceptance criteria
- [ ] `httpx` is added with an exact pin via `uv add`; both `pyproject.toml` and `uv.lock` change.
- [ ] After adding it, `docker build --progress=plain -t telecom .` **reruns** the `uv sync` step. Paste the step line showing it ran, not `CACHED`.
- [ ] A following code-only edit leaves `uv sync` as `CACHED`.
- [ ] Editing `pyproject.toml` by hand (bump the httpx pin) **without** running `uv lock` makes the build fail at `uv sync --locked`. Paste the error, then fix it with `uv lock`.
- [ ] A file named `notes-local.txt` in `projects/telecom/` doesn't reach the image (`docker run --rm telecom ls /app/notes-local.txt` fails), and `.gitignore` is unchanged.

## Hints
- Decide whether `notes-local.txt` should be excluded by a specific pattern or a general one, and keep `.dockerignore` readable.

## Solution
`git diff lesson/M01.04-end solution/M01.04` (created before recording).
