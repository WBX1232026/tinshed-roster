# Assumptions and Decisions

This document records assumptions and decisions made during the project, as required by the Definition of Done.

## Sprint Assumptions

1. Local running is sufficient; no deployment to a server.
2. No TicketNest integration.
3. No real emails or SMS messages are sent.
4. Only sample data is used; no real member privacy is stored.
5. "Confirmed" and "notified" will initially be recorded as two fields or one status in this sprint, with the final decision made during the sprint.
6. Volunteer qualifications, RSA, Blue Card, etc. are not matched in this project; they go only into the backlog.
7. The client accepts either a Python CLI or a web application; no additional requirements are imposed.

## Open Issues

1. Should the final solution be a Python CLI or a web application?
2. Is simple login/permission needed, or is local use sufficient?
3. Should both "confirmed" and "notified" be modelled?
4. Should data be stored in SQLite or a JSON file?
5. Is CSV export needed for printing?
6. How should real volunteer privacy be protected? This time only sample data is used.
7. Judith wants to keep the wall roster. Is the software only the "source of truth" rather than a replacement?

## Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-09-22 | Project kickoff | Align on case requirements |
| 2026-09-23 | Project charter approved | Finalise scope, budget, constraints |
| 2026-09-25 | Requirements and scope approved | User stories, exclusions, backlog |
| 2026-09-30 | Design approved | Data model, rules, architecture |
