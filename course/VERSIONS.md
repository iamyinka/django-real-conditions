# Version manifest

**Validated 2026-11-07** on macOS 26.6.2 (Apple Silicon) with Docker Desktop (Engine 29.3.1, Compose 5.1.1). The containers run Linux arm64. **Re-validated 2026-11-08** after Docker Desktop updated itself to 4.98.0 (Engine 29.9.2, Compose 5.6.1): telecom 16 passed, `tools/stack-check` 17 passed.

This replaces the *proposed* table in the course proposal (section 7.1). Every version below is exact. Each row has one of these statuses:

- **Validated**: installed together with everything else and exercised by a passing test in [`tools/stack-check`](../tools/stack-check/README.md), or by the telecom project's own tests.
- **Pinned**: the exact version is chosen and its source confirmed (registry, release page, licence), but it isn't exercised yet. It gets validated in the module that first uses it, and this file is updated in that module's PR.

A row never moves to *Validated* because a resolver succeeded or a package imported. Something has to actually run.

## How versions change during the course

- Patch updates (6.1.3 → 6.1.4) happen in a normal PR: bump, re-run `stack-check` and the project tests, update this file.
- A minor or major change (Django 6.2, Postgres 19) is a deliberate decision recorded here with a date. It's never mid-module.
- Learners following along later should use **these** versions. The lesson checkpoint tags pin them in `uv.lock` and in the Compose files.

## Runtime and Python packages

| Component | Version | Status | Evidence / notes |
|---|---|---|---|
| Python | **3.14.10** (`python:3.14.10-slim-trixie`) | Validated | All images below. Host Python 3.14.2 is used only for tooling. |
| Django | **6.1.3** | Validated | Telecom suite (16 tests) + stack-check (17 tests). Requires Python ≥ 3.12. |
| psycopg (binary) | **3.3.8** | Validated | `test_versions`, the whole telecom suite |
| Django REST Framework | **3.18.3** | Validated | Declares Django 6.1. `test_drf_filter_and_pagination` |
| django-filter | **26.2** | Validated | Declares Django 6.1 |
| django-cors-headers | **4.9.0** | Validated | Declares only up to Django 6.0; `test_cors_preflight` passes on 6.1.3 |
| whitenoise | **6.12.0** | Validated | Declares only up to 6.0; `test_whitenoise_serves_hashed_static` passes |
| Celery (+ kombu) | **5.7.0** (kombu 5.7.0) | Validated | Real worker round-trip on Redis **and** Valkey |
| redis-py | **8.1.0** | Validated | Via Celery and channels-redis |
| Channels | **4.3.2** | Validated | Declares only up to 6.0; `test_channels_redis_group_broadcast` passes. **Caveat 2** in stack-check README. |
| channels-redis | **4.3.0** | Validated | Same test |
| Daphne | **4.2.3** | Validated | Serves the ASGI app |
| Uvicorn (`[standard]`) | **0.54.0** | Validated | Serves the ASGI app |
| Gunicorn | **26.2.0** | Validated | Serves the WSGI app |
| django-storages (`[s3]`) | **1.14.6** | Validated | Declares only up to Django **5.1** (released 2025-04). Upload, `exists`, presigned GET pass on 6.1.3 against SeaweedFS. **Must set `signature_version="s3v4"`** (caveat 1). Watch for a release; it's the most at-risk dependency. |
| boto3 | **1.43.126** | Validated | Same test. boto3 releases almost daily; patch bumps don't need a manifest decision. |
| Pillow | **13.0.0** | Validated | cp314 wheel available. Thumbnail test. |
| livekit-api (Python server SDK) | **1.2.2** | Validated (token only) | Issues and verifies a room-join JWT. Talking to a running LiveKit server is validated in Module 8. |
| Django built-ins taught | `django.tasks`, `SECURE_CSP`, `MAILERS` | Validated | `test_django_tasks_framework`, CSP in a real browser, telecom settings |

## Test and quality tools

| Component | Version | Status | Evidence / notes |
|---|---|---|---|
| pytest | **9.2.0** | Validated | |
| pytest-django | **4.14.0** | Validated | Declares only up to Django 6.0; all suites pass on 6.1.3 |
| factory_boy | **3.3.3** | Validated | Declares only up to Django 5.1; `DjangoModelFactory` works on 6.1.3 |
| time-machine | **3.6.0** | Validated | |
| Playwright (Python) + Chromium | **1.64.1** | Validated | Real headless Chromium against `live_server`. **Caveat 3** in stack-check README. |
| pytest-playwright | **0.10.0** | Validated | Emits a pytest 9.2 deprecation warning. Harmless. |
| Ruff | **0.17.4** | Validated | pre-commit hook and `ruff check`/`format` |
| pip-audit | **2.10.1** | Validated | stack-check lockfile: *No known vulnerabilities found* (2026-11-07) |
| pre-commit | **4.7.0** (run via `uvx`) | Validated | Hooks: pre-commit-hooks v6.0.0, ruff-pre-commit v0.17.4, gitleaks v8.30.1 |
| gitleaks | **8.30.1** | Validated | `no leaks found` on full history |
| uv | **0.13.7** (`ghcr.io/astral-sh/uv:0.13.7`) | Validated | Every image build, `uv.lock` |

## Services (container images)

| Component | Image | Status | Licence / notes |
|---|---|---|---|
| PostgreSQL | `postgres:18.6-trixie` | Validated | Exclusion constraints, `SKIP LOCKED`. Data volume path changed in 18: mount `/var/lib/postgresql` (telecom M1.6). |
| Redis | `redis:8.8.4-trixie` | Validated | Redis 8 is tri-licensed (RSALv2 / SSPLv1 / **AGPLv3**). Free to use for this course; explained in M5. |
| Valkey | `valkey/valkey:9.0.7-trixie` | Validated | BSD-3-Clause. Drop-in: the identical suite passes with `BROKER_URL=redis://valkey:6379`. |
| S3-compatible storage (local) | `chrislusf/seaweedfs:4.52` | Validated | **Chosen.** Apache-2.0. MinIO is ruled out: its GitHub repository is archived (checked 2026-11-07). Garage v2.5.0 (AGPL-3.0) is a reasonable alternative and is mentioned, not used. |
| Caddy | `caddy:2.11.9` | Pinned | Apache-2.0. Validated in M7 (reverse proxy, TLS). |
| LiveKit server | `livekit/livekit-server:v1.13.11` | Pinned | Apache-2.0. Validated in Module 8. |
| Toxiproxy | `ghcr.io/shopify/toxiproxy:2.13.0` | Pinned | MIT. The Docker Hub image `shopify/toxiproxy` stopped at 2.1.4 (2019). **Use GHCR.** Validated in M6.11. |

## Browser libraries (no build step; vendored files)

| Component | Version | Status | Notes |
|---|---|---|---|
| hls.js | **1.7.4** | Pinned | Module 9 |
| Leaflet | **1.9.4** | Pinned | Still the latest stable release (2023-05). Module 10. |
| livekit-client (JS) | **2.23.0** | Pinned | Module 8 |

## Infrastructure and lab

| Component | Version | Status | Notes |
|---|---|---|---|
| Ubuntu Server LTS | **26.04** | Pinned | Chosen over 24.04: both are LTS, and 26.04 gets the longer support window. Validated in M7 deployment. |
| OpenVPN Community | **2.7.9** | Pinned | **Changed from the proposal's 2.6.x**: 2.7 is the current stable series. Validated in Module 11. |
| Easy-RSA | **3.2.7** | Pinned | Module 11 |
| act (local Actions runner) | **0.2.97** | Validated | Ran `repo-checks` locally while hosted Actions is locked |
| GitHub Actions | `actions/checkout@v7`, `astral-sh/setup-uv@v10.3.3` | Validated with act | **Hosted runs are blocked by an account billing lock.** It must be resolved before Module 7 (M7.3–M7.7). |

## Production recording environment

| Tool | Version |
|---|---|
| macOS | 26.6.2 (arm64) |
| Docker Desktop / Engine / Compose | 4.98.0 / 29.9.2 / 5.6.1 (M0 recorded on these; M1 code validated on 29.3.1 / 5.1.1 too) |
| Git | 2.50.1 |
| FFmpeg | 8.0.1 |
| Kokoro TTS (narration) | 0.9.4, voice `af_heart` |

## Packages that don't declare Django 6.1 yet

Their PyPI classifiers stop before 6.1, but every one passed its stack-check test on Django 6.1.3. These get re-checked whenever this manifest changes:

channels (≤ 6.0), daphne (no Django classifiers), django-cors-headers (≤ 6.0), whitenoise (≤ 6.0), pytest-django (≤ 6.0), factory_boy (≤ 5.1), **django-storages (≤ 5.1)**.

**Fallback:** if any of these breaks on a Django 6.1 patch release, pin Django to the last passing patch. If a fix needs a newer package, update this file in that PR. Django 5.2 LTS remains the documented last resort; no current evidence needs it.
