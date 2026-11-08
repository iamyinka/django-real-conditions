# Pronunciation glossary

This glossary maps each term's **caption** form (shown on screen) to its **spoken** form (the text sent to Kokoro `af_heart`). Phonemes come from misaki's G2P on 2026-11-07. Phonemes show what Kokoro is *asked* to say. Only listening confirms how it actually sounds.

| Caption form | Spoken form | Kokoro phonemes | Status |
|---|---|---|---|
| Django | Django | `ʤˈæŋɡO` | OK. Confirmed by listening in the pilot. |
| exec | exec | `ɛɡzˈɛk` | OK. Confirmed by listening in the pilot. |
| PostgreSQL | **Postgres** | full name garbled: `pˈOstɡəɹɹ ˌɛskjˌuˈɛl` | Always say "Postgres". |
| manage.py | **manage dot py** | `mˈænɪʤ dˈɑt pˈI` | Without "dot", the dot is likely silent. |
| compose.yaml | **compose dot yaml** | `kəmpˈOz dˈɑt jˈæmᵊl` | Write "yaml" in lowercase. Uppercase YAML is spelled out letter by letter. |
| db (service name) | **D B** | `dˌibˈi` | |
| schema | schema | `skˈimə` | OK |
| CLI | C L I | `sˌiˌɛlˈI` | OK |
| localhost | localhost | `lˈOkəlhˌOst` | OK |
| uv | **U V** | `jˈu vˈi` | G2P checked 2026-11-08. Not yet confirmed by listening. |
| pyproject.toml | **pie project dot toml** | `pˈI pɹˈɑʤˌɛkt` | As written, misaki says "pip-roject". |
| psycopg | **psycho P G** | `sˈIkO pˈi ʤˈi` | As written: "sigh-kopg". |
| pytest | **pie test** | `pˈI tˈɛst` | As written: "pie-tist". |
| monorepo | **mono repo** | `mˈɑnO ɹˈipˌO` | As written: stress on "REE". |
| JSON | **Jason** | `ʤˈAsᵊn` | Uppercase is spelled out letter by letter. |
| gitleaks | **git leaks** | `ɡˈɪt lˈiks` | |
| pre-commit | **pre commit** | | |
| /healthz, /readyz | **health Z**, **ready Z** | `hˈɛlθ zˈi`, `ɹˈɛdi zˈi` | |
| /var/lib/postgresql | **var lib Postgres Q L** | `pˈOstɡəɹz kjˈu ˈɛl` | Never read slashes |
| pgdata | **P G data** | `pˈi ʤˈi dˈATə` | |
| .venv | **dot V env** | | |
| WSL, PR, CI, DNS, SMS, API, VPN | Letters with spaces (**W S L**, **P R**, …) | | Space-separated capitals are read as letters |
| psql | **P S Q L** | | |
| 0.0.0.0 / 127.0.0.1 | **one two seven point oh point oh point one** (captions show the digits) | | Spoken "oh" is clearer than "zero" in IPs |

## Terms to verify when a lesson first uses them

These need a G2P check, and a listen, before their first use: uvicorn, gunicorn, Celery, Redis, nginx, Caddy, sqlite, kubectl, OpenVPN, CIDR, ASGI, WSGI, HLS, FFmpeg, WebRTC, STUN, TURN, LiveKit, IndexedDB, CSRF, CORS, JWT, idempotency, PgBouncer.

Add each one to the table above once it's checked. Record the date and whether it's been confirmed by listening.

**How to check:** `tools/kokoro/.venv/bin/python` with `misaki.en.G2P(trf=False, british=False, fallback=EspeakFallback(british=False))`. A word outside misaki's gold/silver lexicon falls back to rules or espeak and needs extra attention. The 2026-11-08 scan of Modules 0–1 found 183 such words. Most were regular inflections; the table above lists the ones that needed a spoken form.
