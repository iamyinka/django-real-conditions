# Exercise — M01.03 Images, containers, and layers

**Start from:** `git switch --detach lesson/M01.03-end`

## Task
Prove three facts about images and containers to yourself, with commands rather than reasoning.

## Acceptance criteria
- [ ] **Writable layers are per container.** Start two containers from `telecom` with `sleep 300` as the command. Create a file in one with `docker exec`. Show it doesn't exist in the other. Delete the first container and show the file is gone.
- [ ] **`EXPOSE` publishes nothing.** Run the image *without* `-p` and show that `curl localhost:8000` from the host fails, while `docker exec <container> python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000').status)"` prints `200`.
- [ ] **The context limits the build.** Add `COPY ../README.md /tmp/` to a scratch copy of the Dockerfile, build it, and paste the error. Explain it in one sentence.

## Hints
- `docker run -d --name a telecom sleep 300` runs a container in the background with a different command.
- Clean up with `docker rm -f a b`.

## Solution
`git show solution/M01.03:course/solutions/M01.03.md` (created before recording) contains the command transcript.
