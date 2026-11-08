# Notes — M01.01 The telecom field-service problem

## Users and what they need

| User | Main jobs | Where they work |
|---|---|---|
| Customer | Report a problem, see progress | Browser, anywhere |
| Support staff | Take phone reports, correct data | Office browser |
| Dispatcher | Triage, assign technicians | Office browser, dashboard |
| Field technician | Update status, notes, photos | Phone browser, often offline |
| Administrator | Accounts, roles, settings | Office browser |

## Ticket states

`reported → triaged → assigned → en_route → on_site → resolved → closed`

Module 2 (M2.8) implements these as a state machine with explicit allowed transitions and a transition history.

## MVP boundary

| In the MVP | Simulated (labeled) | Later (out of scope) |
|---|---|---|
| Customers, sites, subscriptions | Carrier provisioning state | Route optimization |
| Outage reports with deduplication | Outage detection | Native mobile app |
| Ticket state machine, dispatch | SMS gateway | Real SMS providers |
| Offline field updates and photos | | Billing / self-service |
| Notifications via outbox and retries | | Network telemetry |
| Audit history, operational reports | | |

## Success criteria (hypotheses until tested)

| Criterion | Test, and where it's built |
|---|---|
| 100 concurrent duplicates with one idempotency key → 1 ticket | Automated test, M5.4 |
| 2 concurrent overlapping assignments → exactly 1 succeeds | Automated test, M5.1–M5.3 |
| 50 offline operations per network profile → 0 silently lost | Playwright, M6.11 |
| ≤ 1 notification per event under injected duplicates/timeouts; 95% within 60 s | M5.9–M5.11 |
| Dashboard query count constant at 10 vs. 1,000 tickets; p95 < 300 ms locally | M4.3–M4.4 |
| Interrupted photo uploads resume and verify checksums | M6.10 |

## The first issue: anatomy

Real example: [issue #3](https://github.com/iamyinka/django-real-conditions/issues/3).

| Section | Purpose |
|---|---|
| Title | The outcome, in a few words |
| Goal / why | The reason. Reviewers judge the PR against it. |
| Scope | What's included. Here, one line per lesson (M1.2–M1.9). |
| Out of scope | What's deliberately excluded, so it doesn't creep in |
| Acceptance criteria | Checks anyone can run, with the expected result |

Good acceptance criterion: "`docker compose exec web pytest` passes". Bad: "tests are good".

## Tradeoffs and alternatives
- **Simulators vs. vendor sandboxes:** a sandbox is closer to production but needs accounts, may cost money, and can't produce failures on demand. The course uses simulators and labels them.
