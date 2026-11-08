# Notes — M01.04 Build context, .dockerignore, locking, and caching

## Code

### `projects/telecom/Dockerfile` at `lesson/M01.04-end` (changed part)

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project
COPY . .
```

| Line | What it does | When it runs | Why |
|---|---|---|---|
| `UV_COMPILE_BYTECODE=1` | uv compiles installed packages to `.pyc` | Build | Faster container start; done once instead of on every start |
| `UV_LINK_MODE=copy` | uv copies files from its cache instead of hard-linking | Build | The cache mount is a different filesystem; hard links can't cross it (uv would warn and fall back) |
| `COPY pyproject.toml uv.lock ./` | Copies only the two dependency files | Build | The next layer's cache key depends only on these two files |
| `RUN --mount=type=cache,target=/root/.cache/uv` | Mounts a persistent BuildKit cache at uv's cache directory **for this step only** | Build | Downloads survive between builds; the cache isn't saved in the image |
| `uv sync --locked` | Install exactly the locked versions; fail if `uv.lock` is stale | Build | Reproducibility |
| `--no-install-project` | Install dependencies but not the project itself | Build | The code isn't in the image yet, and installing it here would tie this layer to code changes |
| `COPY . .` (now last) | Copies the code | Build | A code edit invalidates only this final, cheap layer |

### `projects/telecom/.dockerignore`

| Pattern | Excludes | Why |
|---|---|---|
| `.venv/` | The host virtualenv | Built for the host OS (useless in Linux) and large: 49 MB / 4,293 files here |
| `**/__pycache__/`, `**/*.py[cod]` | Bytecode | Regenerated anyway |
| `.env`, `.env.*` | Local settings with real values | **Secrets must never reach a layer** |
| `!.env.example` | Re-includes the template | Placeholders only; documents the settings |
| `*.sqlite3`, `media/` | Local data | Data isn't code |
| `.git/`, `.pytest_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/` | Tool and VCS metadata | Not needed at runtime; `.git` can be large |
| `Dockerfile`, `.dockerignore`, `compose*.yaml` | Docker's own files | Editing them shouldn't invalidate the `COPY . .` layer. The builder reads the Dockerfile separately. |

`.dockerignore` vs. `.gitignore`: same pattern style, different job. `.gitignore` decides what Git tracks; `.dockerignore` decides what is sent to the builder. A file can be committed and still excluded from the image, or the other way round.

## Commands

### `docker build --progress=plain -t telecom .`
- `--progress=plain` prints every step's full output (the default collapses it), so you can see `transferring context`, `CACHED`, and step timings.

### `docker run --rm telecom cat /app/.env`
Runs `cat` instead of `CMD` to inspect a file in the image. At `-start` (with a `.env` present) it prints the secret; at `-end`: `cat: /app/.env: No such file or directory`.

### `docker images telecom`
At `-start`: 385 MB. At `-end`: 341 MB.

## How layer caching decides

1. For `RUN`, the cache key is the instruction text plus the parent layer.
2. For `COPY`/`ADD`, it also includes a checksum of the copied files' contents and metadata.
3. The first miss rebuilds that layer **and every layer after it**.

So: order instructions from least to most frequently changing. Base image → system packages → dependency files → dependency install → code.

## Tradeoffs and alternatives
- **Secrets during the build** (a private package index token, for example) belong in `RUN --mount=type=secret`, never in `ARG` or `ENV`, which are recorded in the image metadata.
- **Multi-stage builds** shrink the image further by leaving build tools behind. Module 7 uses one for production.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Rebuild still reinstalls everything | The dependency files changed, or `COPY . .` still comes first | Check the order. `git diff uv.lock`. |
| `the --mount option requires BuildKit` | Old builder | Docker 23+ uses BuildKit by default; keep `# syntax=docker/dockerfile:1` |
| A file is missing in the image that you expected | A `.dockerignore` pattern excluded it | `docker build --progress=plain` and compare the context size, or temporarily remove patterns |
| `.env` still appears in the image | Built before `.dockerignore` existed and a stale image is running | Rebuild, then rotate the secret: it was in a layer |
