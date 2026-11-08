# syntax=docker/dockerfile:1
# The image for the telecom web application (development).
# Build:  docker build -t telecom .    (run in projects/telecom/)

# Base image: Debian 13 "trixie" with Python 3.14.10 preinstalled. "slim" drops
# compilers and docs, which makes the image smaller. Pinning the exact patch
# version means every build starts from the same Python.
FROM python:3.14.10-slim-trixie

# Copy the uv binary out of its official image instead of installing it with pip.
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/

# PYTHONDONTWRITEBYTECODE: don't write .pyc files into the code directory at runtime.
# PYTHONUNBUFFERED: print logs immediately, so `docker logs` shows them in real time.
# UV_PROJECT_ENVIRONMENT: build the virtualenv at /opt/venv, outside /app.
# UV_COMPILE_BYTECODE: precompile dependencies once at build time, for faster startup.
# UV_LINK_MODE=copy: the uv cache is a separate mount, so copy files instead of hard-linking them.
# PATH: put that venv first so `python` means the venv's Python.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Layer caching: Docker reuses a layer only if that instruction and everything
# before it are unchanged. Dependencies change rarely and code changes constantly,
# so copy ONLY the dependency files first and install from them...
COPY pyproject.toml uv.lock ./
# --locked: fail if uv.lock doesn't match pyproject.toml, instead of silently re-resolving.
# --no-install-project: install the dependencies only; the code isn't here yet.
# --mount=type=cache: keep uv's download cache between builds without storing it in the image.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# ...and copy the code last. Editing a .py file now invalidates only this layer.
# The code stays owned by root, so the app user below can read it but not modify it.
COPY . .

# Run as an unprivileged user. If an attacker gets code execution through the app,
# they get a user who can't install packages, change the code, or write to system paths.
# UID/GID default to 1000, the first regular user on most Linux hosts. With a bind mount
# (compose.yaml), files the container creates in /app, such as new migrations, belong to
# this UID on the host. On Linux, build with your own IDs:
#   docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
# Docker Desktop (macOS/Windows) maps ownership automatically.
ARG UID=1000
ARG GID=1000
RUN groupadd --gid "${GID}" app \
    && useradd --uid "${UID}" --gid app --no-create-home --home-dir /nonexistent \
       --shell /usr/sbin/nologin app
# Every instruction after this one, and the running container, use this user.
USER app

# Documentation only: the app listens on 8000 inside the container.
# Publishing it to the host happens at `docker run -p` or in compose.yaml.
# Ports below 1024 would need root; 8000 doesn't.
EXPOSE 8000

# Bind to 0.0.0.0, not 127.0.0.1: inside a container, 127.0.0.1 is the container
# itself, so connections forwarded from the host would never reach the server.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
