# Storyboard — M00.01 How this course works

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Slide: three short "incident" cards appear one at a time | "Saved three times, offline" · "Same technician, same second" · "Deploy without migrate" | diagram `m0-incidents` | 35 |
| 2 | Slide: five project cards in a row, each with an icon and one line | telecom · telehealth · streaming · labtrack · intranet. Project 1 card enlarged at the end | diagram `m0-projects` | 60 |
| 3 | Slide: three numbered points | "Containers, Git, PRs" · "Break it, read it, fix it" · "Every claim checked" | slide | 30 |
| 4 | Diagram: host → web container → db container; the command animates along it | Command shown in full; then `docker compose` highlighted on the host, `python manage.py migrate` in web, the tables in db | diagram `m0-three-places` (reused from the pilot) | 70 |
| 5 | Slide: the three label badges, styled as they'll appear in later lessons | **Simulated** · **Prepared-only** · **Hypothesis** | slide; badge styles from `course/style` | 50 |
| 6 | Terminal (scripted): `git tag -l 'lesson/M01.0*'`, then `git diff --stat lesson/M01.05-start lesson/M01.05-end` | Highlight `-start` / `-end` pairs | repo tags | 55 |
| 7 | Terminal still: the real M1.5 error, then the host/container diagram with "localhost" pointing back into web | `connection to server at "127.0.0.1", port 5432 failed: Connection refused` highlighted | captured during M1.5 verification; diagram `m1-localhost` | 55 |
| 8 | Editor: `course/modules/M01/M01.05/notes.md` scrolling through a command table and a line-by-line table | Highlight the "Part \| Meaning" table, then the "Troubleshooting" table | repo file | 45 |
| 9 | Slide: "You need" / "You don't need" columns | Python, terminal · Docker, advanced Django | slide | 40 |
| 10 | Slide: title card for M0.2 | "Next: your toolchain, verified" | slide | 10 |

## Recording instructions
- Scene 6 is a scripted terminal recording (asciinema-style replay rendered to video) in a fresh clone of `iamyinka/django-real-conditions` after PR #4 is merged. Window: 120×32, font 18 px, dark theme.
- Commands, in order:
  ```bash
  git tag -l 'lesson/M01.0*'
  git diff --stat lesson/M01.05-start lesson/M01.05-end
  ```
- All other scenes are slides rendered with the pilot's slide renderer at 1920×1080.
