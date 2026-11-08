# Storyboard — M00.03 One repository, five independent apps

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Editor file tree, collapsed to the top level | Highlight in turn: `projects/`, `course/`, `docs/`, `scripts/` + `tools/`, `.github/` | repo at `lesson/M00.03-end` | 45 |
| 2 | Slide | "One repository ≠ one application" | slide | 35 |
| 3 | Editor: expand `projects/telecom/` | Highlight `pyproject.toml`, `uv.lock`, `Dockerfile`, `compose.yaml`; caption "release tags: `telecom/v1.0.0`" | repo | 50 |
| 4 | Diagram: five project boxes; a "shared" box appears with arrows to all five, then turns red when one arrow changes | "Copy small things. Share only when duplication costs more than coupling." | diagram `m0-coupling` | 60 |
| 5 | Editor: `.gitignore` scrolled through its sections | Section headers highlighted: secrets, environments, databases/media, rendered media | `.gitignore` | 45 |
| 6 | Terminal | `cp projects/telecom/.env.example projects/telecom/.env` → `git status` (no `.env`) → `git check-ignore -v projects/telecom/.env` → `git check-ignore -v projects/telecom/.env.example` (no output: tracked) → `git check-ignore -v --no-index projects/telecom/.env.example` → `.gitignore:4:!.env.example` | live terminal | 90 |
| 7 | Terminal, **Simulated** badge | Create `projects/leak_demo.py` with the fake token → `git add` → `uvx pre-commit run gitleaks --files projects/leak_demo.py` → `Failed`, `RuleID: github-pat`, `File: projects/leak_demo.py`, `Line: 1` | live terminal | 75 |
| 8 | Slide: timeline "commit → delete commit → clone still has it" | "Fix = revoke + reissue. History rewrite is second." | slide | 45 |
| 9 | Editor: `.gitattributes`, then `.editorconfig` | `* text=auto eol=lf` highlighted | repo files | 45 |
| 10 | Slide | "Next: the professional Git loop" | slide | 10 |

## Recording instructions
- Start from a clean clone at `lesson/M00.03-end` with `uvx pre-commit install` already run.
- Scene 7: generate the fake token on camera with
  `printf 'GITHUB_TOKEN=ghp_%s\n' "$(python3 -c 'import secrets,string;print("".join(secrets.choice(string.ascii_letters+string.digits) for _ in range(36)))')" > projects/leak_demo.py`
  After the scene: `git rm --cached projects/leak_demo.py && rm projects/leak_demo.py`. Verified on 2026-11-08: gitleaks 8.30.1 reports `github-pat` and exits 1.
- Scene 6: delete the `.env` copy afterwards (`rm projects/telecom/.env`) unless you continue straight into Module 1.
