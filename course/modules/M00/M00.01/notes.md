# Notes — M00.01 How this course works

A detailed reference for the lesson. The video covers the essentials, and these notes explain every line.

## The five projects

| # | Directory | Business | What makes it hard |
|---|---|---|---|
| 1 | `projects/telecom` | Telecom operations and field service | Offline work, concurrency, background jobs, deployment |
| 2 | `projects/telehealth` | Telehealth consultations (synthetic data) | Time zones, double booking, private files, video calls |
| 3 | `projects/streaming` | Streaming and offline learning | Large uploads, transcoding, adaptive streaming, offline downloads |
| 4 | `projects/labtrack` | Lab logistics and live tracking (synthetic data) | State machines, append-only events, live location over WebSockets |
| 5 | `projects/intranet` | Private intranet over LAN and OpenVPN | Networking, private HTTPS, VPN access and revocation |

Each project is independent: its own Compose file, dependencies, database, and release tags.

## WHAT / WHERE / WHY

| Question | Example answer for `docker compose exec web python manage.py migrate` |
|---|---|
| WHAT | Applies Django migrations that haven't run yet |
| WHERE | Typed on the **host**; `python manage.py migrate` runs **in the web container**; tables change **in the db container** |
| WHY | The schema must match the code before the code serves requests. Running it explicitly (not on every restart) keeps it a deliberate step |

## Honesty labels

| Label | Meaning | Example |
|---|---|---|
| **Simulated** | A deliberate stand-in for something real | The fake SMS gateway in M5.11 |
| **Prepared-only** | Configuration or steps shown but not run in the recording | Some VPN client steps in Module 11 |
| **Hypothesis** | Expected but not measured yet | A performance prediction before the measurement lesson |
| *(no label)* | It ran, and what you see is what happened | |

## Commands

### `git tag -l 'lesson/M01.0*'`
- **Working directory:** the repository root
- **Where it runs:** host
- **Prerequisites:** a clone of the course repository

| Part | Meaning |
|---|---|
| `git tag` | Git's tag subcommand. With no arguments it lists tags. |
| `-l` | List mode, filtered by a pattern |
| `'lesson/M01.0*'` | A glob pattern. The single quotes stop your shell from expanding `*` against file names before Git sees it. |

- **Expected output:** `lesson/M01.02-end`, `lesson/M01.02-start`, … (sorted alphabetically)

### `git diff --stat lesson/M01.05-start lesson/M01.05-end`

| Part | Meaning |
|---|---|
| `git diff A B` | The changes needed to turn commit A into commit B |
| `--stat` | Summarize: files changed and lines added/removed, not the full diff |

- **Expected output:** one line per changed file and a summary line.

### Following along with checkpoints

```bash
git switch --detach lesson/M01.05-start   # jump to the start of M1.5
# ...follow the lesson...
git diff lesson/M01.05-end                # compare your working tree with the reference end state
```

`--detach` is needed because a tag isn't a branch. To keep your work, create a branch: `git switch -c my-m1.5`.

## Tradeoffs and alternatives
- Tags vs. one branch per lesson: tags are immutable and don't clutter the branch list. A branch per lesson would invite commits onto the reference history.

## Troubleshooting
- `fatal: invalid reference` when switching to a tag: fetch tags first with `git fetch --tags`.
