# The image for the telecom web application (development).
# Build:  docker build -t telecom .    (run in projects/telecom/)

# Base image: Debian 13 "trixie" with Python 3.14.10 preinstalled. "slim" drops
# compilers and docs, which makes the image smaller. Pinning the exact patch
# version means every build starts from the same Python.
FROM python:3.14.10-slim-trixie

# Copy the uv binary out of its official image instead of installing it with pip.
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/

# PYTHONDONTWRITEBYTECODE: don't write .pyc files into the code directory.
# PYTHONUNBUFFERED: print logs immediately, so `docker logs` shows them in real time.
# UV_PROJECT_ENVIRONMENT: build the virtualenv at /opt/venv, outside /app.
# PATH: put that venv first so `python` means the venv's Python.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy the whole build context, then install the locked dependencies.
COPY . .
RUN uv sync --locked

# Documentation only: the app listens on 8000 inside the container.
# Publishing it to the host happens at `docker run -p` or in compose.yaml.
EXPOSE 8000

# Bind to 0.0.0.0, not 127.0.0.1: inside a container, 127.0.0.1 is the container
# itself, so connections forwarded from the host would never reach the server.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
