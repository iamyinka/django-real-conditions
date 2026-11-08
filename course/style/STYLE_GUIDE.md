# Course style guide

These rules apply to every lesson script, storyboard, set of notes, and exercise.

## Voice

The narration should sound like a thoughtful developer teaching a colleague: warm, plain, and precise. It is not a corporate training video and not a hype reel.

| Do | Don't |
|---|---|
| Use contractions ("it's", "doesn't") | Write stiff, formal prose |
| Vary sentence length; keep most sentences under 25 words | Write a run of long, clause-heavy sentences |
| Explain one idea at a time | Stack three new terms into one sentence |
| Use transitions that follow the reasoning: "Let's see what happens when the connection drops." | Use filler transitions: "Moving on…", "Next up…" |
| Say why a line exists | Read code aloud symbol by symbol |
| Admit limits: "This won't survive a closed tab." | Over-promise: "This makes it bulletproof." |
| Name the place: "in the web container", "in the browser" | Use a vague "it runs" |

**Avoid** scripted enthusiasm ("Awesome!"), forced jokes, a repeated "In this lesson we will…" opener, and reading slides word for word.

## WHAT / WHERE / WHY

Every command, code block, setting, and decision answers three questions:

- **WHAT** it does, or what behavior changes.
- **WHERE** it runs or belongs: the host, a container, the browser, a worker, the database, a network boundary, or a specific file or directory.
- **WHY** we're doing it: the business or engineering problem it solves, and the alternatives.

**Before a command:** state the prerequisites and the working directory.
**After a command:** state the expected output, any side effects, and how to verify it worked. If a failure is meaningful, say how to recover.

## Explaining code and commands

- Introduce code in small sections, and highlight the lines under discussion in the storyboard.
- Explain commands piece by piece: the program, subcommand, flags and their values, positional arguments, paths, quoting, pipes and redirection, and environment variables.
- Explain imports, decorators, class inheritance, field options, signatures, defaults, and return values. Say which behavior comes from Python, Django, Docker, the browser, or another dependency.
- Say *when* each part executes: at import time, at request time, during migration, or in a worker.
- When code repeats, give a one-line reminder of what it does. Explain changed lines fully.
- The full line-by-line explanation lives in the lesson's `notes.md`. The narration covers the important parts naturally. It doesn't read the notes aloud.
- If a lesson would run past 15 minutes, split it. Don't rush the explanation.

## The nine-step teaching sequence

Each major concept goes through these steps. They may be spread across consecutive lessons.

1. Business problem.
2. Plain explanation and an analogy.
3. Where the analogy breaks down.
4. A small runnable example.
5. Apply it to the project.
6. Show a failure or common mistake.
7. Diagnose it and fix it.
8. Tradeoffs and when to use it.
9. Exercise with acceptance criteria; the solution goes on a separate tag.

## Honesty labels

On screen and in notes, mark anything **Simulated**, **Prepared-only**, or **Hypothesis**. Mark anything untested as untested. Never present a configuration file as proof that a system works.

On screen they're pill badges (defined in `tools/course/produce/slides.py`, `BADGES`): **Simulated** amber (`#78350f` / `#fde68a`), **Prepared-only** blue (`#1e3a8a` / `#bfdbfe`), **Hypothesis** violet (`#4c1d95` / `#ddd6fe`). No badge means it ran.

## Writing for text-to-speech (Kokoro, voice `af_heart`)

The course narration uses the voice approved in the pilot. Each script line has a **caption** form (what's written on screen) and, only when needed, a **spoken** form.

- Use the spoken forms in `PRONUNCIATION.md` for file names, abbreviations, and symbols.
- Never put raw code in the spoken text. Describe it instead: "the dash-dash-check flag", "manage dot py".
- One sentence per line. The audio pipeline synthesizes each sentence separately.
- Scene breaks (`---`) produce a longer pause and mark where the visual changes.
- Every track gets automated checks (loudness, clipping, silences, and a speech-recognition transcription check) **and** a human listen. Automated checks never replace listening.
