# Notes — M01.09 Non-root containers, permissions, and secrets in development

## Code

### `Dockerfile` additions at `lesson/M01.09-end`

```dockerfile
ARG UID=1000
ARG GID=1000
RUN groupadd --gid "${GID}" app \
    && useradd --uid "${UID}" --gid app --no-create-home --home-dir /nonexistent \
       --shell /usr/sbin/nologin app
USER app
```

| Line | What it does | When it runs | Why |
|---|---|---|---|
| `ARG UID=1000` / `ARG GID=1000` | Build-time variables with defaults | Build | Linux users can pass their own IDs; 1000 is the first regular user on most distributions |
| `groupadd --gid "${GID}" app` | Creates group `app` | Build | |
| `useradd --uid … --gid app` | Creates user `app` in that group | Build | |
| `--no-create-home --home-dir /nonexistent` | No home directory | Build | Nothing to write to; the app doesn't need one |
| `--shell /usr/sbin/nologin` | No interactive login | Build | Defence in depth |
| `USER app` | Later instructions and the container's processes run as `app` | Build and runtime | The point of the lesson |
| *(placement after `COPY . .`)* | The code was copied as root, so it's owned by root | Build | `app` can read the code, not modify it |

`ARG` values aren't secret: they're visible in `docker history`. Never pass secrets as build arguments.

## Commands

| Command | Expected output (verified) |
|---|---|
| `docker compose exec web id` | `uid=1000(app) gid=1000(app) groups=1000(app)` |
| `docker compose exec web touch /x` | `touch: cannot touch '/x': Permission denied` |
| `docker compose exec web touch /opt/venv/x` | `Permission denied` |
| `docker compose exec web pip install six` | `Defaulting to user installation…` then `ERROR: … [Errno 13] Permission denied: '/nonexistent'` |
| `docker run --rm --entrypoint "" telecom-web sh -c 'echo x >> /app/manage.py'` | `sh: 1: cannot create /app/manage.py: Permission denied` (image only, no bind mount) |
| `docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)` | Rebuild with your host IDs (Linux) |
| `docker history --no-trunc telecom-web \| grep -ciE "dev-only\|SECRET_KEY\|PASSWORD"` | `0` |

### `docker run` vs. `docker compose run` for inspecting an image

| | `docker run IMAGE` | `docker compose run SERVICE` |
|---|---|---|
| Volumes | None unless you add `-v` | **The service's volumes, including bind mounts** |
| Environment | None unless you add `-e` | The service's `env_file` and `environment` |
| Use it to inspect | The image as built | The service as configured |

## Where development secrets are, and aren't

| Place | Contains secrets? | Enforced by |
|---|---|---|
| Git history | No | `.gitignore`, gitleaks (pre-commit + CI) |
| Image layers | No | `.dockerignore` (`.env`, `.env.*`) |
| Image metadata (`ENV`, `ARG`) | No | Review: nothing secret in the Dockerfile |
| Container environment at runtime | **Yes** | That's where they're meant to be in dev |
| `docker inspect`, `exec … env`, debug pages, crash reports | **Yes, visible** | Not protected; acceptable only for throwaway dev values |

## Tradeoffs and alternatives
- **Rootless Docker / user namespaces** map container root to an unprivileged host user. That's complementary to `USER`, not a replacement.
- **Compose `secrets:`** mounts files under `/run/secrets/`, out of the environment. That's better against accidental logging, and used in production setups (Module 7).
- **`--read-only` root filesystem**: an even stronger guard. It needs writable `tmpfs` mounts for anything that writes. Considered in Module 7.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Linux: can't edit a migration the container created | File owned by uid 1000 ≠ your uid | Rebuild with `--build-arg UID=$(id -u) --build-arg GID=$(id -g)`; fix existing files with `sudo chown` |
| `PermissionError` writing to `/app/...` without a bind mount | Code is root-owned by design | Write data to a volume, not the code directory |
| `.pytest_cache` warnings in the image | pytest can't write its cache | Harmless; or `-p no:cacheprovider` |
