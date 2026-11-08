# Notes — M01.06 Volumes: bind mounts vs. named volumes

## Code

### `compose.yaml` changes at `lesson/M01.06-end`

```yaml
services:
  web:
    # ...
    volumes:
      - .:/app
  db:
    # ...
    volumes:
      - pgdata:/var/lib/postgresql

volumes:
  pgdata:
```

| Line | Kind | Meaning | Why |
|---|---|---|---|
| `- .:/app` | Bind mount | `host_path:container_path`. A path starting with `.` or `/` is a bind mount. `.` is relative to `compose.yaml`. | Code edits appear instantly; runserver reloads |
| `- pgdata:/var/lib/postgresql` | Named volume | `volume_name:container_path`. A bare name means a volume. | Data outlives containers |
| top-level `volumes: pgdata:` | Declaration | Compose creates `telecom_pgdata` if it doesn't exist | Named volumes must be declared |

### Why `/var/lib/postgresql` and not `/var/lib/postgresql/data`

| Fact | Evidence (postgres:18.6-trixie) |
|---|---|
| The image declares its volume at `/var/lib/postgresql` | `docker image inspect … -f '{{json .Config.Volumes}}'` → `{"/var/lib/postgresql":{}}` |
| Data lives in a version-specific subfolder | `PGDATA=/var/lib/postgresql/18/docker` |
| Mounting the old path fails | Exit code 1, `Error: in 18+, these Docker images are configured to store database data in a format which is compatible with "pg_ctlcluster"…`, plus a pointer to docker-library/postgres#1259 |

Why the change: version-specific directories allow `pg_upgrade --link` between major versions inside one mount.

## Commands

### `docker compose exec db psql -U telecom -d telecom -c "…"`

| Part | Meaning |
|---|---|
| `exec db` | Run in the running db container |
| `psql` | Postgres' command-line client, shipped in the image |
| `-U telecom` | Database user (`POSTGRES_USER`) |
| `-d telecom` | Database name (`POSTGRES_DB`) |
| `-c "…"` | Run this SQL and exit |

No password is needed: inside the container, `psql` connects over the Unix socket, which the image trusts for local connections.

### `docker volume ls`
Lists volumes. Anonymous volumes have 64-character hex names; named ones appear as `telecom_pgdata`.

### `docker compose down` vs. `docker compose down -v`

| Command | Containers | Network | Named volumes | Anonymous volumes |
|---|---|---|---|---|
| `down` | Removed | Removed | **Kept** | Kept, but orphaned: the next `up` creates a new one |
| `down -v` | Removed | Removed | **Removed** | Removed |

### `docker compose logs -f web`
Follows the web container's logs. `-f` = follow; Ctrl+C stops following, not the container.

## Three kinds of storage

| | Writable layer | Named volume | Bind mount |
|---|---|---|---|
| Lives | Inside the container | Docker's storage area (inside the Docker Desktop VM on macOS/Windows) | Your host folder |
| Survives container removal | No | Yes | Yes (it's your files) |
| Typical use | Temporary files | Databases | Code in development |
| Performance on macOS/Windows | Fast | Fast | Slower (crosses the VM boundary) |

## Tradeoffs and alternatives
- **Bind-mounting the database folder** (`./pgdata:/var/lib/postgresql`) works but causes host permission problems and is slower on macOS. Named volumes are the norm.
- **Bind mounts in production:** don't. Production runs the code baked into the image (Module 7).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| db container exits 1 right after `up`, with the "in 18+" message | Mounted `/var/lib/postgresql/data` | Mount `/var/lib/postgresql` |
| Data "disappears" after `down`/`up` | No named volume (anonymous) | Add the named volume |
| Data disappears and you didn't expect it | Someone ran `down -v` | Restore from backup (M7.8). In dev: `migrate` again. |
| Disk filling up with mystery volumes | Orphaned anonymous volumes | `docker volume ls -f dangling=true`, inspect, then remove the ones you're sure about |
| Code edits don't show up | No bind mount, or editing a different folder | `docker compose exec web ls -la /app` |
