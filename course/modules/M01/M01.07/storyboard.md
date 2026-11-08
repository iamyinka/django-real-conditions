# Storyboard — M01.07 Management commands inside containers

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | The approved pilot's animated command breakdown (host → exec → web → manage.py) | Command segments highlighted in turn | pilot slides (`pilot/out/af_heart/slides`) | 50 |
| 2 | Diagram: web → network → db; then terminal: second `migrate` → `No migrations to apply.` | `django_migrations` table highlighted in db | diagram `m0-three-places`; live | 40 |
| 3 | Terminal | `docker compose down -v && docker compose up -d` → `docker compose restart web` → `docker compose exec web python manage.py showmigrations auth` → `[ ] 0001_initial` … → `migrate` → `[X] 0001_initial` … | live | 75 |
| 4 | Terminal | `docker compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.count(), 'user(s)')"` → `0 user(s)` | live | 40 |
| 5 | Terminal | `docker compose exec -e DJANGO_SUPERUSER_PASSWORD=dev-only-admin web python manage.py createsuperuser --noinput --username admin --email admin@example.test` → `Superuser created successfully.`; the shell one-liner → `1 user(s)` | live | 65 |
| 6 | Terminal, two commands side by side | `docker compose exec web hostname` → `398045903df8`; `docker compose run --rm --no-deps web hostname` → `5b8ee71067d0` | live | 55 |
| 7 | Terminal | `docker compose exec web pytest -q` → `10 passed`; `… manage.py check` → `System check identified no issues (0 silenced).`; `… makemigrations --check --dry-run` → `No changes detected`; `docker compose logs -f web` | live | 75 |
| 8 | Editor: `projects/telecom/README.md` | "Everyday commands: what runs where" and "Troubleshooting" tables | `README.md` at `-end` | 35 |
| 9 | Slide | "Next: started ≠ ready" | slide | 15 |

## Recording instructions
- Record at `lesson/M01.07-start`. Scene 3 deletes the dev database on purpose (`down -v`).
- Container IDs in scene 6 will differ. The point is that they differ from each other.
- Outputs verified on 2026-11-07 against this checkpoint: restart leaves `[ ]`; `migrate` applies 18; `createsuperuser --noinput` with the env var succeeds; `shell -c` prints the count; `exec`/`run` hostnames differ; `10 passed`; check and `makemigrations --check` clean.
- Scene 1 reuses the pilot visuals so this lesson matches the approved narration standard.
