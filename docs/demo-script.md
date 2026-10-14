# Demo Script (10 minutes)

> Owner: Yao Tingran (Business/Requirements Lead). Used for the A3 formal acceptance demonstration (10-min demo + 5-min Q&A).

## Timing overview

| Time | Section |
|---|---|
| 0:00–1:00 | Problem and product |
| 1:00–2:00 | Team and approach |
| 2:00–5:30 | Live demo (core workflow) |
| 5:30–7:00 | One-role rule and views |
| 7:00–8:30 | Testing and CI |
| 8:30–10:00 | Process, Jira/GitHub, lessons |

## 0:00–1:00 — Problem and product

- "Tinshed Players stage up to four shows a year, eight performances each."
- "Rostering today is a Facebook group, group texts, an exercise book and the coordinator's notebook — so we get double-booked volunteers, unfilled roles, and phone calls asking who is on."
- "Tinshed Roster is one place for the season, its performances, and who is crewing each — so the coordinator can see the holes, and a volunteer can see what they have been put down for."

## 1:00–2:00 — Team and approach

- Team of three: Zhang Yixuan (PM), Yao Tingran (Business/Requirements), Li Qize (Technical).
- Agile/Scrum: user stories with acceptance criteria, a sprint backlog, PR-based workflow, CI on every change.

## 2:00–5:30 — Live demo (core workflow)

1. **Create volunteers** — add "Col Hendricks" (name + phone). Show it appears in the list.
2. **Create a production and performances** — "The Weather House", add a Friday-evening performance with date and start time.
3. **Define a crew call** — Bar 1, Sound Op, Usher ×2; note call times (crew 60 min, FOH/box office 45 min before curtain).
4. **Assign volunteers** — assign Col to Bar 1; point out the assignment starts "unconfirmed", then confirm it.

## 5:30–7:00 — One-role rule and views

5. **One-role rule** — try to assign Col to a second role on the same performance; show the refusal message naming the conflict.
6. **Roster gap view** — show filled vs open positions; point out the Usher role still open.
7. **Personal roster view** — open Col's view; show only his assignments, in date/time order.

## 7:00–8:30 — Testing and CI

- `pytest` — 96 tests, 17 files, all passing (show the terminal output).
- CI (GitHub Actions) runs the suite + a smoke step on Python 3.10 and 3.12 for every push and PR.

## 8:30–10:00 — Process, Jira/GitHub, lessons

- GitHub: feature branches + pull requests for every change; the `docs/` folder holds requirements, user stories, test plan/results, traceability matrix, UAT.
- Jira: backlog, sprint, meeting minutes, test and UAT issues.
- **Lessons learned:** the one-role rule taught us to nail acceptance criteria before coding; the two-layer (store/service + web) split kept the app testable.

## Q&A prep (5 min)

- "What would you do next?" → qualification matching (PBI-1), validation hardening, a web UI, cross-performance conflict checks.
- "Why SQLite?" → single-file, zero-config, satisfies the file-based persistence requirement.
