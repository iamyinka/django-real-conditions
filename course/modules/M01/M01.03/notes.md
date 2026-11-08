# Notes — M01.03 Images, containers, and layers: the Dockerfile

## Code

### `projects/telecom/Dockerfile` at `lesson/M01.03-end`

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.14.10-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . .
RUN uv sync --locked
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

| Line | What it does | When it runs | Why it's written this way |
|---|---|---|---|
| `# syntax=docker/dockerfile:1` | Selects the Dockerfile frontend (parser) version 1.x | Build start | Enables newer features such as `RUN --mount` (used in M1.4) |
| `FROM python:3.14.10-slim-trixie` | The base image: Debian 13 with CPython 3.14.10 | Build | Exact patch pin = reproducible base. `slim` omits compilers and docs. |
| `COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/` | Copies two binaries out of the uv image | Build | No pip install of uv; the version is pinned by the tag |
| `ENV PYTHONDONTWRITEBYTECODE=1` | No `.pyc` files written next to the code at runtime | Build sets it; applies at runtime | Keeps a bind-mounted code folder clean (M1.6) |
| `ENV PYTHONUNBUFFERED=1` | stdout/stderr unbuffered | Runtime | Logs show up in `docker logs` immediately |
| `ENV UV_PROJECT_ENVIRONMENT=/opt/venv` | uv creates the venv at `/opt/venv` | Build (`uv sync`) | Outside `/app`, so mounting code over `/app` later doesn't hide it |
| `ENV PATH="/opt/venv/bin:$PATH"` | That venv's `python` comes first | Build and runtime | `python manage.py …` uses the right interpreter without activation |
| `WORKDIR /app` | Creates `/app` and makes it the current directory | Build and runtime | Relative paths and `CMD` run from here |
| `COPY . .` | Copies the build context into `/app` | Build | Simple, but it copies **everything**, including `.venv` (fixed in M1.4) |
| `RUN uv sync --locked` | Installs dependencies exactly as locked | Build | `--locked` fails if `uv.lock` is out of date, instead of re-resolving |
| `EXPOSE 8000` | Metadata: "this image listens on 8000" | Never executes | Documentation for humans and tools; publishing is `-p` |
| `CMD [...]` | The default command for containers | Container start | JSON (exec) form: no shell in between, so signals reach Python directly |

## Commands

### `docker build -t telecom .`
- **Working directory:** `projects/telecom/`
- **Where it runs:** the CLI on the host sends the context to the daemon; the build runs in the daemon (a Linux VM on macOS/Windows).

| Part | Meaning |
|---|---|
| `docker build` | Build an image from a Dockerfile |
| `-t telecom` | Tag (name) the result `telecom:latest` |
| `.` | The build context: this folder is sent to the builder. `Dockerfile` is looked for here by default. |

- **Expected output:** BuildKit steps `[1/5] FROM …` to `[5/5] RUN uv sync --locked`, then `naming to docker.io/library/telecom:latest`.
- **Verify:** `docker images telecom` → about 385 MB at this checkpoint.

### `docker history telecom`
Lists layers newest-first with their size and creating instruction. At this checkpoint: `COPY . .` 51 MB, `RUN … uv sync` 61.8 MB.

### `docker run --rm -p 127.0.0.1:8001:8000 -e DJANGO_SECRET_KEY=dev-only telecom`

| Part | Meaning |
|---|---|
| `docker run` | Create and start a container from an image |
| `--rm` | Delete the container when it stops |
| `-p 127.0.0.1:8001:8000` | Publish: host address `127.0.0.1`, host port `8001` → container port `8000` |
| `-e DJANGO_SECRET_KEY=dev-only` | Set an environment variable in the container. The secret isn't in the image. |
| `telecom` | The image. With no command after it, `CMD` runs. |

- **Expected:** runserver output; `http://localhost:8001/` shows "The install worked successfully!"; the log line `"GET / HTTP/1.1" 200 12149`.
- **Stop it:** Ctrl+C. `--rm` removes the container.

### `docker run --rm telecom python -c "import sys, django; print(sys.version.split()[0], django.get_version())"`
Anything after the image name **replaces** `CMD`. Output: `3.14.10 6.1.3`.

## Two addresses, two places

| Address | Where | Meaning |
|---|---|---|
| `0.0.0.0:8000` in `CMD` | Inside the container | Listen on all the container's interfaces, including the one Docker forwards to |
| `127.0.0.1:8000` inside | Inside the container | Only the container's own loopback. Forwarded traffic never arrives: `curl: (52) Empty reply from server`. |
| `127.0.0.1:8001` in `-p` | On the host | Only your machine can connect. Without it, `-p 8001:8000` listens on every host interface, and Docker's published ports can bypass a host firewall. |

## Tradeoffs and alternatives
- **`slim` vs. `alpine`:** Alpine uses musl libc. Many Python wheels are built for glibc, so Alpine can mean compiling from source. `slim` is the safer default.
- **`runserver` in the image:** development only. Module 7 builds a production image with Gunicorn.
- **Running as root:** this image still runs as root. M1.9 fixes that.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Bind for 127.0.0.1:8001 failed: port is already allocated` | Another container (or process) already uses host port 8001 | `docker ps` to find it; stop it or pick another host port |
| `ImproperlyConfigured: Set the DJANGO_SECRET_KEY…` | Forgot `-e` | Add `-e DJANGO_SECRET_KEY=…` |
| `Invalid HTTP_HOST header` | You browsed to an address that isn't in `ALLOWED_HOSTS` | Use `localhost` or `127.0.0.1` |
| `error: The lockfile at uv.lock needs to be updated` | `pyproject.toml` changed without `uv lock` | Run `uv lock` on the host and rebuild |
