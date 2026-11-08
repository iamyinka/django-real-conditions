# Storyboard — M01.01 The telecom field-service problem

| Scene | Visual | On-screen text / highlight | Source | Approx. duration |
|---|---|---|---|---|
| 1 | Illustrated map: a street cabinet, 200 house icons lighting up red, phone and web icons | "Fiber cut · 200 customers · 1 technician in a basement" | diagram `m1-outage-map` | 45 |
| 2 | Five persona cards | Customer · Support · Dispatcher · Technician · Admin | slide | 40 |
| 3 | Flow diagram; then the state machine as a row of pills | `reported → triaged → assigned → en_route → on_site → resolved → closed` | diagram `m1-ticket-states` (proposal §4) | 75 |
| 4 | The same flow, with four red markers | Duplicate · Race · Offline · Once-only notification; each tagged with its module (M5, M5, M6, M5) | diagram | 45 |
| 5 | Two-column slide | **In:** customers, sites, subscriptions, tickets, dispatch, offline updates + photos, notifications, audit, reports · **Later:** routing, native app, billing, telemetry | slide | 50 |
| 6 | Architecture diagram with three boxes badged **Simulated** | Provisioning · Outage detection · SMS gateway | diagram `m1-architecture` (proposal §5) | 55 |
| 7 | Table slide, badge **Hypothesis** | 100 duplicates → 1 ticket · 2 assignments → 1 winner · 50 offline ops → 0 lost | slide | 45 |
| 8 | Browser: issue #3 on GitHub, scrolled section by section | Title, Goal, Scope (M1.2–M1.9), Out of scope, Acceptance criteria | `iamyinka/django-real-conditions#3` | 80 |
| 9 | Slide | "Next: starting from nothing" | slide | 10 |

## Recording instructions
- Scene 8 shows the real issue #3 (now closed by PR #4). Show it as it was written. The closed state is fine and gets a caption: "closed by PR #4 when Module 1's code merged".
- Diagrams are rendered from the proposal's Mermaid sources with the course palette.
