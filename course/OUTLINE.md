# Course outline: Django Under Real Conditions

**Final outline, Milestone 2 (2026-11-07).** 13 modules, 136 lessons, **1,747 min (about 29.1 hours)** of planned video. Lessons run 8–15 minutes. This is the authoritative lesson list. It supersedes section 3 of the proposal, and every change from the proposal is listed below.

Exact tool and library versions are in [`VERSIONS.md`](VERSIONS.md).

## How to read this outline

- **ID** `M<module>.<lesson>` is used everywhere: script filenames, storyboards, notes, exercises, and commit messages.
- **Checkpoint tags.** Each lesson that changes project code has `lesson/MXX.YY-start` and `lesson/MXX.YY-end` tags, with module and lesson zero-padded (M1.7 → `lesson/M01.07-…`). A learner can `git checkout lesson/M01.07-start`, follow the lesson, and diff against `-end`. Lessons that change no code (M0.1, M1.1, M6.12, …) get only an `-end` tag on the current state, so every lesson has a known starting point.
- **Solutions** live on `solution/MXX.YY` tags, never on `main` next to the exercise.
- **Release tags** (`telecom/v1.0.0`, …) mark shipped versions of a project. They're separate from lesson tags.
- **Labels** follow the style guide. **Simulated** means a stand-in for something real (a fake SMS gateway, a route simulator, scripted review comments). **Prepared-only** means configuration or steps shown but not executed in the recording. **Hypothesis** means stated but not yet measured. **Synthetic data** means no real people or specimens.
- **Needs** names an outside dependency that must be in place before recording that lesson.

## Every lesson ships with

1. A script (`course/modules/MXX/MXX.YY/script.md`) using the style guide's WHAT / WHERE / WHY structure.
2. A storyboard with the shot list and on-screen text.
3. Companion notes that explain the code and commands line by line.
4. An exercise with acceptance criteria, and a solution tag.
5. Narration (Kokoro `af_heart`, -16 LUFS), captions (WebVTT), and an automated transcription check. These are produced after the scripts are approved, not in Milestone 2.

## Changes from the approved proposal

Lesson count, order, and timings are unchanged. The changes come from validation work in Milestone 2:

| Lesson | Change | Why |
|---|---|---|
| M1.6 | Adds the PostgreSQL 18 data-directory change | Tested: the old `/var/lib/postgresql/data` mount makes `postgres:18.6` exit with code 1 |
| M1.8 | Adds `/healthz` vs. `/readyz`, `pg_isready` over TCP, and the DNS failure mode | Observed: socket `pg_isready` reported ready during first-time init; a stopped `db` fails name resolution |
| M1.9 | Adds UID/GID build arguments for Linux bind mounts | Needed for the non-root image to work with Linux hosts |
| M5.12 | "To be checked" replaced with what was validated | `django.tasks` `@task` + `.enqueue()` passes on Django 6.1.3 |
| M6.11 | Names Toxiproxy 2.13.0 from GHCR | The Docker Hub image stopped at 2.1.4 (2019) |
| M8.7 | Uses Django's built-in CSP (`SECURE_CSP`) | Validated in real Chromium: an inline script is blocked |
| M8.8 | Local storage is SeaweedFS, and SigV4 is set explicitly | The MinIO repository is archived; django-storages + boto3 presigned with SigV2 by default |
| M11.10 | OpenVPN 2.7.9 (was 2.6.x) | 2.7 is the current stable series |
| M7.3–M7.7 | Marked *Needs: hosted GitHub Actions* | The account's Actions billing lock must be cleared before recording |

## Production status

| Module | Code | Scripts | Audio / video |
|---|---|---|---|
| M0 | n/a (repo foundations merged in PR #2) | In progress (Milestone 2) | After script approval |
| M1 | M1.2–M1.9 done, tagged (PR #4) | In progress (Milestone 2) | After script approval |
| M2–M12 | Not started | Not started | Not started |

---

## Module 0: Orientation and the professional loop

4 lessons, 46 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M0.1 | How this course works | 8 | The five projects and the WHAT/WHERE/WHY habit. How to read the labels for simulated, prepared-only, and measured work. How exercises and checkpoints work. | `lesson/M00.01-start` → `-end` |  |
| M0.2 | Your toolchain, verified | 12 | Install and verify Python, uv, Docker, Compose, Git, and an editor. Covers macOS, Linux, and WSL2 differences, and what to do when a check fails. | `lesson/M00.02-start` → `-end` |  |
| M0.3 | One repository, five independent apps | 12 | The monorepo layout and why shared code stays small. What never gets committed (secrets, media, databases, virtual environments) and how `.gitignore` enforces that. | `lesson/M00.03-start` → `-end` |  |
| M0.4 | The professional Git loop | 14 | The full loop: issue, branch, commits, PR, review, CI, merge, deploy, tag. Protected `main`, branch naming, and commit messages. Merge vs. squash vs. rebase, and why squash-merge is the course default. Lesson checkpoint tags vs. release tags. | `lesson/M00.04-start` → `-end` |  |

## Module 1: Project 1 kickoff, from an empty folder to containers

10 lessons, 121 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M1.1 | The telecom field-service problem | 10 | Users, workflows, the MVP boundary, and what will be simulated (provisioning, outages, SMS). Turning the problem into the first issue with acceptance criteria. | `lesson/M01.01-start` → `-end` |  |
| M1.2 | Starting from nothing | 12 | `startproject`, an explicit settings layout, settings read from environment variables, and the first run. What `manage.py` actually does. | `lesson/M01.02-start` → `-end` |  |
| M1.3 | Images, containers, and layers: the Dockerfile | 14 | Writing the Django `Dockerfile` line by line. Images vs. containers and what a layer is. Where the build runs compared with where the container runs. | `lesson/M01.03-start` → `-end` |  |
| M1.4 | Build context, `.dockerignore`, locking, and caching | 12 | Locking dependencies with `uv.lock`. Ordering layers so the cache works for you. Why a bloated build context slows builds and can leak secrets into the image. | `lesson/M01.04-start` → `-end` |  |
| M1.5 | Compose: Django and PostgreSQL | 13 | Services, networks, and service names vs. `localhost`. What a published port actually means. Diagnosing a "connection refused" error. | `lesson/M01.05-start` → `-end` |  |
| M1.6 | Volumes: bind mounts vs. named volumes | 11 | Where data lives. What survives `docker compose down` and what `down -v` destroys. PostgreSQL 18 moved its data directory: mounting the old `/var/lib/postgresql/data` path makes the container exit, so the lesson mounts `/var/lib/postgresql`. Containers aren't durable storage. | `lesson/M01.06-start` → `-end` |  |
| M1.7 | Management commands inside containers | 12 | `docker compose exec web python manage.py migrate`, explained part by part. Shells, logs, and tests inside containers. Why a restart doesn't apply migrations. | `lesson/M01.07-start` → `-end` |  |
| M1.8 | Health checks, readiness, and startup order | 12 | `healthcheck`, `depends_on: condition: service_healthy`, and the gap between "started" and "ready". `/healthz` vs. `/readyz`. A bounded `wait_for_db` retry. Why `pg_isready` must use TCP during first-time init, and why a stopped service fails DNS rather than refusing connections. | `lesson/M01.08-start` → `-end` |  |
| M1.9 | Non-root containers, permissions, and secrets in development | 11 | Running as a non-root user and the file-ownership problems that causes with bind mounts on Linux (UID/GID build arguments). `.env` files vs. real secret stores, and who can read environment variables. | `lesson/M01.09-start` → `-end` |  |
| M1.10 | Shipping the skeleton: first issue, branch, and PR | 14 | Staging only selected changes, writing a commit message, reviewing your own diff, opening a PR, and squash-merging. Review feedback in this lesson is labeled as simulated. | `lesson/M01.10-start` → `-end` | Simulated: review feedback |

## Module 2: Project 1, modeling the business

10 lessons, 126 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M2.1 | How a request becomes a response | 14 | The full journey: browser, proxy, Gunicorn (WSGI), middleware, URL resolver, view, ORM, and back. Drawn as a request timeline with real timings. | `lesson/M02.01-start` → `-end` |  |
| M2.2 | Middleware order and request tracing | 13 | Writing a request-ID middleware. Why the order of middleware changes what each one can see. Log correlation. | `lesson/M02.02-start` → `-end` |  |
| M2.3 | Exceptions and error responses | 11 | What Django does with 404s, 500s, and `PermissionDenied`. Logging errors without leaking data. Custom error pages. | `lesson/M02.03-start` → `-end` |  |
| M2.4 | Customers, sites, and subscriptions | 14 | Model relationships, choosing field options, and naming. What each field option does to the database. | `lesson/M02.04-start` → `-end` |  |
| M2.5 | Migrations in depth | 13 | What `makemigrations` and `migrate` each do. Reading the SQL with `sqlmigrate`. Applying migrations to a live database safely. | `lesson/M02.05-start` → `-end` |  |
| M2.6 | Deletion behavior has business consequences | 11 | `CASCADE` vs. `PROTECT` vs. `SET_NULL`. Soft deletion vs. archiving. The "who deleted all the tickets?" failure. | `lesson/M02.06-start` → `-end` |  |
| M2.7 | Three layers of validation | 14 | Form validation, model `clean()`, and database constraints. Which layer protects against what, and why the database is the last line of defense. | `lesson/M02.07-start` → `-end` |  |
| M2.8 | Tickets as a state machine | 13 | Defining allowed transitions, rejecting invalid ones, and recording transition history. | `lesson/M02.08-start` → `-end` |  |
| M2.9 | Reproducible sample data | 11 | A management command plus factories with a fixed seed. Why fixtures exported from someone's laptop go stale. | `lesson/M02.09-start` → `-end` |  |
| M2.10 | Migration merge conflicts | 12 | Two branches both add migrations. Diagnosing the conflict, using `makemigrations --merge`, or rebasing and renumbering. | `lesson/M02.10-start` → `-end` |  |

## Module 3: Project 1, who can do what

8 lessons, 101 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M3.1 | Authentication, authorization, sessions, and cookies | 13 | What a session actually is, where it's stored, and what the cookie carries. | `lesson/M03.01-start` → `-end` |  |
| M3.2 | CSRF: the attack and the defense | 13 | Demonstrating a forged request, how the CSRF token blocks it, and what CSRF protection doesn't cover. | `lesson/M03.02-start` → `-end` |  |
| M3.3 | Roles with groups and permissions | 12 | Support staff, dispatchers, technicians, and customers. Model permissions vs. business roles. | `lesson/M03.03-start` → `-end` |  |
| M3.4 | Object-level permissions | 14 | Technicians see only their assigned tickets. Customers see only their own sites. Building it, then exploiting an ID in the URL, then fixing it. | `lesson/M03.04-start` → `-end` |  |
| M3.5 | QuerySets as security boundaries | 12 | Scoping every lookup through the user. Why checking permission after fetching the object is a common bug. | `lesson/M03.05-start` → `-end` |  |
| M3.6 | Session expiry, logout, and shared devices | 12 | Cookie flags (`Secure`, `HttpOnly`, `SameSite`), idle vs. absolute expiry, and what logout really clears. | `lesson/M03.06-start` → `-end` |  |
| M3.7 | Audit history | 13 | An append-only audit table: who, what, when, and from where. What to keep out of the audit trail. | `lesson/M03.07-start` → `-end` |  |
| M3.8 | Testing permissions with a matrix | 12 | A table-driven test that checks every role against every action, so an access hole shows up as a failing test. | `lesson/M03.08-start` → `-end` |  |

## Module 4: Project 1, QuerySets and database performance

8 lessons, 99 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M4.1 | QuerySets are lazy | 12 | When SQL actually runs: iteration, slicing, `bool()`, and `len()`. Watching queries happen in the shell. | `lesson/M04.01-start` → `-end` |  |
| M4.2 | Query caching and its traps | 10 | When results get reused, when they don't, and stale data inside long-lived objects. | `lesson/M04.02-start` → `-end` |  |
| M4.3 | Finding N+1 queries | 13 | The dispatcher dashboard gets slow. Measuring queries with `assertNumQueries` and the debug toolbar. | `lesson/M04.03-start` → `-end` |  |
| M4.4 | `select_related`, `prefetch_related`, and `Prefetch` | 13 | Fixing the dashboard and checking that the query count stays flat as the data grows. | `lesson/M04.04-start` → `-end` |  |
| M4.5 | Indexes and `EXPLAIN ANALYZE` | 14 | Reading a PostgreSQL query plan, adding an index, measuring the change, and the cost indexes add to writes. | `lesson/M04.05-start` → `-end` |  |
| M4.6 | Operational reporting | 13 | Aggregation, annotation, and time buckets for open-ticket age and technician workload. | `lesson/M04.06-start` → `-end` |  |
| M4.7 | Pagination: offset vs. keyset | 11 | Why deep offset pages get slow, and how keyset pagination avoids it. | `lesson/M04.07-start` → `-end` |  |
| M4.8 | Caching the report safely | 13 | Cache keys, invalidation, and Redis as a cache. Preventing one user's private response from being served to another. | `lesson/M04.08-start` → `-end` |  |

## Module 5: Project 1, concurrency, transactions, and background work

12 lessons, 154 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M5.1 | Two dispatchers, one technician | 13 | A race condition reproduced live with two concurrent requests. | `lesson/M05.01-start` → `-end` |  |
| M5.2 | Transactions | 13 | `atomic`, autocommit, savepoints, and what rolls back. Side effects such as emails don't roll back with the database. | `lesson/M05.02-start` → `-end` |  |
| M5.3 | Locking strategies | 14 | `select_for_update`, conditional `UPDATE … WHERE`, and unique constraints. Deadlocks and lock timeouts. | `lesson/M05.03-start` → `-end` |  |
| M5.4 | Idempotency keys | 14 | Duplicate tickets from double clicks and retries. Storing the key and its response. Behavior when a request with the same key is still in flight. | `lesson/M05.04-start` → `-end` |  |
| M5.5 | Processes, threads, and async I/O | 14 | A working mental model of how Gunicorn workers, threads, and an event loop each handle concurrent requests. | `lesson/M05.05-start` → `-end` |  |
| M5.6 | The GIL, accurately | 12 | What the GIL limits, how native extensions release it, what free-threaded builds change, and what remains unchanged. | `lesson/M05.06-start` → `-end` |  |
| M5.7 | Why a thread inside a request isn't background work | 11 | A demonstration: the worker restarts and the work silently disappears. | `lesson/M05.07-start` → `-end` |  |
| M5.8 | Celery and Redis | 14 | Brokers, workers, and queue messages. `acks_late`, visibility timeouts, and the duplicate deliveries they make possible. | `lesson/M05.08-start` → `-end` |  |
| M5.9 | The transactional outbox | 14 | Recording the intent to notify in the same transaction as the business change, then having a relay publish it. | `lesson/M05.09-start` → `-end` |  |
| M5.10 | Retries, backoff with jitter, and idempotency limits | 13 | Retry policies, dead letters, and why "exactly once" rarely holds once an outside provider is involved. | `lesson/M05.10-start` → `-end` |  |
| M5.11 | A simulated SMS provider | 12 | A labeled fake SMS gateway with configurable failures, timeouts, and duplicate deliveries. Delivery status tracking. | `lesson/M05.11-start` → `-end` | Simulated: SMS gateway |
| M5.12 | Django's task interface vs. Celery | 10 | Django's built-in `django.tasks` framework (`@task`, `.enqueue()`, configurable backends; validated on 6.1.3 with the immediate backend). What it leaves to the backend you choose, compared with Celery, and how to decide. | `lesson/M05.12-start` → `-end` |  |

## Module 6: Project 1, offline field work

12 lessons, 160 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M6.1 | A technician's day without signal | 11 | Offline requirements, what offline can't do, and how much data is safe to keep on the device. | `lesson/M06.01-start` → `-end` |  |
| M6.2 | An API with Django REST Framework | 14 | Serializers, viewsets, and routers, explained line by line. | `lesson/M06.02-start` → `-end` |  |
| M6.3 | API permissions, filtering, pagination, and versioning | 14 | Reusing the permission rules from Module 3 in the API. URL vs. header versioning. | `lesson/M06.03-start` → `-end` |  |
| M6.4 | API authentication; CORS vs. CSRF | 14 | Session vs. token authentication for a same-origin offline app. What CORS controls and what it doesn't. | `lesson/M06.04-start` → `-end` |  |
| M6.5 | Service workers | 13 | Scope, lifecycle, updates, and caching the app shell. Debugging in DevTools. | `lesson/M06.05-start` → `-end` |  |
| M6.6 | An IndexedDB operation queue | 14 | Storing what the technician meant to do as queued operations rather than snapshots of rows. Writing a small wrapper around IndexedDB. | `lesson/M06.06-start` → `-end` |  |
| M6.7 | Synchronization | 14 | Ordering, client operation IDs as idempotency keys, server acknowledgments, and partial success. | `lesson/M06.07-start` → `-end` |  |
| M6.8 | Explicit conflicts | 14 | Detecting conflicts with version numbers and showing a resolution screen. Why last write wins silently loses data. | `lesson/M06.08-start` → `-end` |  |
| M6.9 | Photos: compression and metadata | 12 | Compressing on the device with canvas, reading and stripping EXIF, and the privacy cost of location metadata. | `lesson/M06.09-start` → `-end` |  |
| M6.10 | Resumable chunked uploads | 14 | Upload sessions, chunk offsets, and checksums, sent through Django because P1 photos are small. P3 shows the direct-to-storage alternative. | `lesson/M06.10-start` → `-end` |  |
| M6.11 | Network failure lab | 15 | Covers latency, low bandwidth, disconnects, an expired login during sync, and a response that's lost after a successful commit. Conditions are produced with Toxiproxy 2.13.0 (from GHCR) and Chrome DevTools throttling, and each one says which tool produced it. | `lesson/M06.11-start` → `-end` | Simulated: network conditions |
| M6.12 | Packets, chunks, segments, messages, and tasks | 11 | Five different units of data, side by side: network packets, upload chunks, video segments, WebSocket messages, and queue messages. Why they aren't interchangeable. | `lesson/M06.12-start` → `-end` |  |

## Module 7: Project 1, test, ship, and operate

10 lessons, 126 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M7.1 | Test strategy | 13 | Unit, integration, and browser tests with Playwright. Which behaviors are critical enough to deserve tests. | `lesson/M07.01-start` → `-end` |  |
| M7.2 | The local quality gate | 10 | Ruff formatting and linting, `makemigrations --check`, and `manage.py check --deploy`. | `lesson/M07.02-start` → `-end` |  |
| M7.3 | A CI pipeline | 14 | GitHub Actions with PostgreSQL and Redis service containers, building and tagging the image, and a registry. | `lesson/M07.03-start` → `-end` | Needs: Hosted GitHub Actions |
| M7.4 | Failing CI and review changes | 12 | Reading a failure, fixing it on the branch, updating the branch from `main`, and responding to review comments. | `lesson/M07.04-start` → `-end` | Needs: Hosted GitHub Actions |
| M7.5 | Production settings and the production image | 13 | A multi-stage build, static files, `DEBUG=False`, and the production server command. | `lesson/M07.05-start` → `-end` | Needs: Hosted GitHub Actions (GHCR push) |
| M7.6 | A Linux server with Compose, Caddy, and HTTPS | 15 | The reverse proxy, certificates, firewall, and getting secrets onto the server. | `lesson/M07.06-start` → `-end` | Needs: A Linux server + domain |
| M7.7 | Deploy, migrate, and verify | 13 | The deployment runbook, migration timing, smoke checks, logs, and basic monitoring. | `lesson/M07.07-start` → `-end` | Needs: A Linux server + domain; hosted Actions |
| M7.8 | Backups and a restore drill | 13 | `pg_dump` and restore, media backups, and actually running a restore. An untested backup doesn't count as a backup. | `lesson/M07.08-start` → `-end` |  |
| M7.9 | Reverts, hotfixes, and rollback limits | 13 | Reverting code doesn't undo migrations. Backward-compatible migrations and a hotfix branch. | `lesson/M07.09-start` → `-end` |  |
| M7.10 | Releases and the P1 retrospective | 10 | Tagging `telecom/v1.0.0`, measuring the success metrics, and listing what remains. | `lesson/M07.10-start` → `-end` |  |

## Module 8: Project 2, telehealth consultations

14 lessons, 187 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M8.1 | The problem, the boundaries, and the disclaimer | 11 | Synthetic data only, no compliance claims, and why a teaching prototype isn't a clinical system. Defining the MVP. | `lesson/M08.01-start` → `-end` | Synthetic data |
| M8.2 | A fresh project, faster | 12 | Repeating the P1 setup concisely, with full written documentation. What changes for this project. | `lesson/M08.02-start` → `-end` |  |
| M8.3 | Patients, clinicians, appointments, and time zones | 14 | Storing UTC, displaying local time, DST traps, and a clinician's availability. | `lesson/M08.03-start` → `-end` |  |
| M8.4 | Preventing double bookings | 14 | Exclusion constraints, compared with locking. Two patients booking the same slot at once. | `lesson/M08.04-start` → `-end` |  |
| M8.5 | Intake forms that survive interruptions | 13 | Partial saves, validation, and recovering a resubmitted form after a dropped connection. | `lesson/M08.05-start` → `-end` |  |
| M8.6 | Patient and clinician access boundaries | 14 | Assignment-based access and testing it adversarially. | `lesson/M08.06-start` → `-end` |  |
| M8.7 | Hardened sessions | 14 | Cookie flags, short idle timeouts, re-authentication for sensitive actions, Django's built-in Content Security Policy (`SECURE_CSP`, shown blocking an inline script in a real browser), and risks on shared devices. | `lesson/M08.07-start` → `-end` |  |
| M8.8 | Private documents and signed URLs | 14 | Private object storage (SeaweedFS locally), short-lived presigned URLs, content types, and integrity checks. Why `signature_version="s3v4"` must be set explicitly. | `lesson/M08.08-start` → `-end` |  |
| M8.9 | Slow uploads and reconnects | 13 | Direct-to-storage uploads with progress and retries, and recovering from interrupted requests. | `lesson/M08.09-start` → `-end` |  |
| M8.10 | Audit events and logs that don't leak | 12 | Recording an event without its sensitive content. Scrubbing logs and testing that nothing leaks. | `lesson/M08.10-start` → `-end` |  |
| M8.11 | Reliable reminders | 14 | Scheduling, cancellation, rescheduling, DST, and how long a reminder takes to arrive, using the outbox from P1. | `lesson/M08.11-start` → `-end` |  |
| M8.12 | WebRTC explained | 14 | Signaling, ICE, STUN, TURN, and SFUs. Why video never goes through Django. | `lesson/M08.12-start` → `-end` |  |
| M8.13 | LiveKit integration | 14 | Django checks the appointment and issues a short-lived room token. LiveKit carries the media. Handling webhooks. | `lesson/M08.13-start` → `-end` | Local LiveKit server |
| M8.14 | Retention, deletion, and the limits of revocation; ship it | 14 | Object versions, backups, and why deletion and revocation take time to take effect. Deploy and tag `telehealth/v1.0.0`. | `lesson/M08.14-start` → `-end` |  |

## Module 9: Project 3, streaming and offline learning

14 lessons, 187 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M9.1 | Learners on expensive connections | 11 | Users, the MVP (HLS online plus a progressive file for offline), and the cost drivers. | `lesson/M09.01-start` → `-end` |  |
| M9.2 | How video works | 14 | Containers, codecs, bitrates, keyframes, and GOPs. Why file size and quality trade off against each other. | `lesson/M09.02-start` → `-end` |  |
| M9.3 | Progressive vs. segmented playback | 13 | HTTP range requests and `206 Partial Content`, demonstrated with `curl`. | `lesson/M09.03-start` → `-end` |  |
| M9.4 | Large direct uploads | 14 | S3 multipart uploads with presigned part URLs. Django handles authorization; the bytes go straight to storage. | `lesson/M09.04-start` → `-end` |  |
| M9.5 | Resumability, checksums, and completion | 14 | Resuming after a browser reload, verifying each part, completing the upload, and cleaning up abandoned uploads. | `lesson/M09.05-start` → `-end` |  |
| M9.6 | FFmpeg transcoding, line by line | 15 | Every flag in the transcoding command, run and checked with `ffprobe`. | `lesson/M09.06-start` → `-end` |  |
| M9.7 | Orchestrating transcodes | 14 | Worker states, progress, retries, cancellation, and keeping heavy work off web workers. | `lesson/M09.07-start` → `-end` |  |
| M9.8 | HLS adaptive streaming | 14 | Bitrate ladders, master and media playlists, and `hls.js` vs. native playback. DASH as an alternative. | `lesson/M09.08-start` → `-end` |  |
| M9.9 | Captions, thumbnails, audio-only, and low-bandwidth mode | 13 | WebVTT, poster frames, an audio-only rendition, and a data-saver mode. | `lesson/M09.09-start` → `-end` |  |
| M9.10 | Playback authorization, CDNs, and caching | 14 | Signed URLs vs. signed cookies, cache keys, and what a CDN can and can't protect. | `lesson/M09.10-start` → `-end` |  |
| M9.11 | Saving and resuming playback progress | 11 | Throttled saves, the last write winning, and sending progress with `sendBeacon` when a tab closes. | `lesson/M09.11-start` → `-end` |  |
| M9.12 | Offline downloads | 15 | Service worker, Cache Storage vs. OPFS, quotas, eviction, and persistent storage requests. | `lesson/M09.12-start` → `-end` |  |
| M9.13 | Resumable downloads and a support matrix | 13 | Range-based resume, backoff with jitter, cancellation, and the tested browser matrix. | `lesson/M09.13-start` → `-end` |  |
| M9.14 | The limits of offline revocation and copy protection; ship it | 12 | What signed URLs can't enforce once a file is on the device, and where DRM fits. Metrics, deploy, and tag `streaming/v1.0.0`. | `lesson/M09.14-start` → `-end` |  |

## Module 10: Project 4, laboratory logistics and live tracking

14 lessons, 186 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M10.1 | The synthetic specimen workflow | 11 | Users, the MVP, the disclaimer, and what counts as a later extension. | `lesson/M10.01-start` → `-end` | Synthetic data |
| M10.2 | Facility isolation | 14 | Multi-tenant scoping, assignment-based permissions, and an ID-guessing exploit followed by its fix. | `lesson/M10.02-start` → `-end` |  |
| M10.3 | Collection requests and specimen labels | 12 | One request covering many specimens, label identifiers, and uniqueness. | `lesson/M10.03-start` → `-end` |  |
| M10.4 | State machines and invalid transitions | 14 | Collection and specimen lifecycles, a transition table, and testing every invalid edge. | `lesson/M10.04-start` → `-end` |  |
| M10.5 | Custody events | 14 | An append-only event log, device time vs. server time, and clock skew. | `lesson/M10.05-start` → `-end` |  |
| M10.6 | Results, revisions, and corrections | 13 | Versioned results, correction reasons, and why a published result is never overwritten in place. | `lesson/M10.06-start` → `-end` |  |
| M10.7 | Offline events, duplicates, and out-of-order messages | 14 | Event IDs, sequence numbers, and reconciling events that arrive late. | `lesson/M10.07-start` → `-end` |  |
| M10.8 | WSGI vs. ASGI and sync vs. async | 14 | Running on an ASGI server, `sync_to_async`, and async views. When async helps and when it doesn't. | `lesson/M10.08-start` → `-end` |  |
| M10.9 | Browser geolocation and a route simulator | 13 | Permission prompts, secure contexts, accuracy, and why tracking stops when the tab is suspended. The route simulator is clearly labeled. | `lesson/M10.09-start` → `-end` | Simulated: route |
| M10.10 | Location ingestion | 13 | Throttling, freshness, accuracy filtering, retention windows, and privacy. | `lesson/M10.10-start` → `-end` |  |
| M10.11 | Authorized WebSocket subscriptions | 14 | Channels consumers and groups, and checking permissions at connect time and on every subscription. WebSockets deliver updates; they don't collect GPS. | `lesson/M10.11-start` → `-end` |  |
| M10.12 | Reconnects, resynchronization, and choosing a transport | 14 | Missed messages, rebuilding state from the server after a reconnect, and polling vs. SSE vs. WebSockets. | `lesson/M10.12-start` → `-end` |  |
| M10.13 | Alerts | 14 | Detecting delays, deduplicating alerts, acknowledgment, and escalation with a defined limit. | `lesson/M10.13-start` → `-end` |  |
| M10.14 | The map UI; ship it | 12 | Leaflet, tile usage policy, and accessibility. Deploy and tag `labtrack/v1.0.0`. | `lesson/M10.14-start` → `-end` |  |

## Module 11: Project 5, a private intranet over LAN and OpenVPN

14 lessons, 179 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M11.1 | The intranet problem and the lab topology | 11 | Users and the MVP. Which steps are executed and which are prepared-only, with each marked as it comes up. | `lesson/M11.01-start` → `-end` | Prepared-only steps marked |
| M11.2 | Networking you actually need | 15 | Private IP addresses, CIDR, ports, interfaces, routes, and return paths. | `lesson/M11.02-start` → `-end` |  |
| M11.3 | Inspecting your lab and choosing subnets | 11 | Reading your existing routes and choosing subnets that don't conflict with your home, office, or Docker networks. | `lesson/M11.03-start` → `-end` |  |
| M11.4 | The portal app | 14 | Announcements, department documents, service requests, and departments. | `lesson/M11.04-start` → `-end` |  |
| M11.5 | Department permissions and private documents | 12 | Scoped access and private file delivery. | `lesson/M11.05-start` → `-end` |  |
| M11.6 | Binding privately and firewall rules | 13 | Listening addresses, Docker's published-port behavior that can bypass a host firewall, and firewall rules. | `lesson/M11.06-start` → `-end` |  |
| M11.7 | Internal DNS and HTTPS with a private CA | 14 | A `.internal` hostname, distributing CA trust, and the extra certificate needed to use HTTPS on a raw IP address. | `lesson/M11.07-start` → `-end` |  |
| M11.8 | Reverse proxy and Django host checks | 13 | Caddy, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, proxy headers, and keeping the database private. | `lesson/M11.08-start` → `-end` |  |
| M11.9 | Why the VPN runs in a VM | 11 | TUN devices, privileges, routing, and Docker Desktop's VM layer. When a container is fine and when it isn't. | `lesson/M11.09-start` → `-end` | Needs: 2–3 Linux VMs |
| M11.10 | The OpenVPN server | 15 | Building the certificate authority with Easy-RSA 3.2.7, and the OpenVPN 2.7 server configuration line by line. | `lesson/M11.10-start` → `-end` | Needs: 2–3 Linux VMs |
| M11.11 | Client profiles and tunnel modes | 14 | Handling profiles safely, split vs. full tunneling, and routed vs. NAT access. | `lesson/M11.11-start` → `-end` | Needs: 2–3 Linux VMs |
| M11.12 | Revoking access, twice | 13 | Revoking a VPN certificate, updating the CRL, ending live sessions, and revoking Django access separately. | `lesson/M11.12-start` → `-end` | Needs: 2–3 Linux VMs |
| M11.13 | Troubleshooting | 13 | Disconnects, logs, DNS, MTU, and asymmetric routing. What Django sessions do when the VPN drops. | `lesson/M11.13-start` → `-end` | Needs: 2–3 Linux VMs |
| M11.14 | Shared responsibility; ship it | 10 | Where host, network, and Django security each begin and end. Tag `intranet/v1.0.0`. | `lesson/M11.14-start` → `-end` |  |

## Module 12: Capstone

6 lessons, 75 min

| ID | Lesson | Min | What the learner sees and does | Checkpoint tags | Label / dependency |
|---|---|---|---|---|---|
| M12.1 | The capstone brief | 10 | Extend the intranet with offline field inspections for remote staff behind the VPN, including photos, background report generation, and outbox notifications. | `lesson/M12.01-start` → `-end` |  |
| M12.2 | Design review | 13 | Architecture, tradeoffs, the MVP boundary, and metrics, written up as a design document. | `lesson/M12.02-start` → `-end` |  |
| M12.3 | Building the capstone | 15 | Reusing the patterns from earlier projects deliberately rather than copying code. | `lesson/M12.03-start` → `-end` |  |
| M12.4 | Failure drills | 15 | The VPN drops mid-sync, a login expires, a worker crashes, and a response is lost after commit. | `lesson/M12.04-start` → `-end` |  |
| M12.5 | Operations | 13 | Monitoring, a backup and restore drill, the release, and the verification manifest. | `lesson/M12.05-start` → `-end` |  |
| M12.6 | A checklist for engineering judgment | 9 | The decisions that recurred across all five projects. | `lesson/M12.06-start` → `-end` |  |
