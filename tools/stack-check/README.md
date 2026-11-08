# stack-check: proof for the version manifest

This isn't a course project. It's a small Django app that pins **every Python package the course uses**, at the exact versions in [`course/VERSIONS.md`](../../course/VERSIONS.md), and exercises each one against real services: Postgres 18, Redis 8 or Valkey 9, SeaweedFS S3, a Celery worker, three app servers, and headless Chromium.

A dependency resolver succeeding doesn't prove compatibility. These tests do.

## Run it

```bash
cd tools/stack-check
docker compose --profile run run --rm tests                       # Redis 8 as broker/channel layer
BROKER_URL=redis://valkey:6379 docker compose --profile run up -d worker gunicorn uvicorn daphne
BROKER_URL=redis://valkey:6379 docker compose --profile run run --rm tests   # same suite on Valkey 9
docker compose --profile run down -v
```

The first build downloads Chromium for Playwright (about 600 MB of image layers).

## What each test proves

| File | Test | Proves |
|---|---|---|
| `test_core.py` | `test_versions` | Django 6.1.3 talks to a PostgreSQL 18.x server through psycopg 3 |
| | `test_drf_filter_and_pagination` | DRF 3.18.3 + django-filter 26.2: filtering and page-number pagination |
| | `test_cors_preflight` | django-cors-headers 4.9.0 answers a preflight for an allowed origin |
| | `test_csp_header_from_django_core` | Django's built-in CSP middleware (`SECURE_CSP`) sets the header |
| | `test_whitenoise_serves_hashed_static` | whitenoise 6.12.0 manifest storage hashes and serves static files |
| | `test_exclusion_constraint_rejects_overlap` | `ExclusionConstraint` + `btree_gist` reject overlapping bookings |
| | `test_select_for_update_skip_locked` | `select_for_update(skip_locked=True)` on Postgres 18 |
| | `test_time_machine_freezes_auto_now` | time-machine 3.6.0 + factory_boy 3.3.3 with `auto_now_add` |
| | `test_django_tasks_framework` | Django's `django.tasks` `@task` + `ImmediateBackend` |
| | `test_livekit_token` | livekit-api 1.2.2 issues a room-join JWT |
| `test_services.py` | `test_celery_roundtrip_through_real_worker` | Celery 5.7.0: task → broker → separate worker process → result backend |
| | `test_channels_redis_group_broadcast` | Channels 4.3.2 + channels-redis 4.3.0: group message reaches another socket |
| | `test_pillow_thumbnail_to_s3_and_presigned_get` | Pillow 13 thumbnail → django-storages 1.14.6 → SeaweedFS; SigV4 presigned GET works |
| | `test_app_servers_serve_requests` ×3 | gunicorn 26.2.0 (WSGI), uvicorn 0.54.0 and daphne 4.2.3 (ASGI) serve the app |
| `test_browser.py` | `test_django_csp_blocks_inline_script_in_real_chromium` | Playwright 1.64.1 drives Chromium against `live_server`; the browser enforces Django's CSP |

## Known caveats found while building this

These are real findings, and the course teaches them where they come up.

1. **SigV2 presigned URLs by default.** With boto3 1.43 and django-storages 1.14.6, `FileField.url` produced `AWSAccessKeyId=…&Signature=…` (legacy SigV2) until `signature_version: "s3v4"` was set. → M8 / M9.
2. **Channels consumers touch the database on connect** (`close_old_connections`). Under pytest-django, a consumer test needs `@pytest.mark.django_db(transaction=True)`. That test also failed when it ran after `test_core.py` in the same process, but passed alone and with its own file. This wasn't investigated further; files run as separate processes. → M10.
3. **Playwright's sync API + pytest-django**: the test DB setup and teardown raise `SynchronousOnlyOperation`. The browser test process sets `DJANGO_ALLOW_ASYNC_UNSAFE=true` and runs separately. Never set it in application settings. → M6.11.
4. **The Celery worker is its own process.** `stackcheck/celery.py` must set `DJANGO_SETTINGS_MODULE` itself. → M5.
5. **Warnings seen** (none affect results): pytest-playwright 0.10.0 triggers pytest 9.2's `PytestRemovedIn10Warning` (a session-scoped fixture defined as an instance method); whitenoise warns that `STATIC_ROOT` doesn't exist before `collectstatic`.
