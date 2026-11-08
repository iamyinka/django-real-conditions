# Exercise — M01.08 Health checks, readiness, and startup order

**Start from:** `git switch --detach lesson/M01.08-end`, then `git switch -c exercise/m1.8`

## Task
Module 4 adds Redis as a cache. The dispatcher dashboard can work without the cache (slowly), but can't work without the database. Extend readiness to report both, with the right status code.

## Acceptance criteria
- [ ] `/readyz` returns `{"status": "ok", "checks": {"database": "ok", "cache": "ok"}}` and 200 when both work.
- [ ] With the cache failing, it returns **200** with `"status": "degraded"` and `"cache": "error"`. With the database failing, **503**, whatever the cache does.
- [ ] Use Django's cache framework (`django.core.cache.cache`), not a Redis client, so it works with any cache backend. For this exercise, configure `LocMemCache` in settings.
- [ ] Tests cover all four combinations (db ok/fail × cache ok/fail) by patching, without a real Redis.
- [ ] Error details are logged, never returned.

## Hints
- `cache.set(key, value, timeout)` then `cache.get(key)` is a real round-trip. Use a key unlikely to collide.

## Solution
`git diff lesson/M01.08-end solution/M01.08` (created before recording).
