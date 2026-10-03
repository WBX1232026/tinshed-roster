# Handover Document

## 1. What was delivered against scope

- **Volunteers** (US-1, US-2, US-3): create, find, update and deactivate a volunteer; deactivation preserves existing assignments.
- **Productions and performances** (US-4, US-5): create a production, add/change/remove performances, list them in date and time order.
- **Crew calls** (US-6): record roles and the number needed per performance.
- **Assignments** (US-7, US-8, US-9): assign, change and remove assignments; new assignments default to "unconfirmed"; the one-role-per-performance rule is enforced.
- **Views** (US-10, US-11): roster view showing filled and open positions; personal roster view listing a volunteer's own assignments.
- **Requirements artefacts**: requirements analysis and scope definition (`docs/requirements.md`), user stories with acceptance criteria (`docs/user-stories.md`), meeting minutes (`docs/meeting-minutes.md`), and an acceptance testing record (`docs/acceptance-testing.md`).

## 2. What was not delivered, and why

- Out-of-scope items (from `docs/requirements.md` and the README) are deferred to the product backlog and were not part of this sprint: ticketing and box office sales, membership fees and renewals, RSA/Blue Card/qualification matching, rehearsals and casting, venue booking clashes, grant acquittal, equipment inventory, email/SMS notifications, volunteer shift swaps, hours reporting, and TicketNest integration.
- No in-scope story was knowingly dropped; any partial work is listed under Known issues below.

## 3. Setup and run instructions from GitHub

```bash
git clone https://github.com/WBX1232026/tinshed-roster.git
cd tinshed-roster
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py         # run the application
pytest                     # run the tests
```

## 4. Known issues and limitations

- Input validation is lightweight: empty names and duplicate contact details are not yet rejected with dedicated messages.
- The interface is text-driven (CLI); no web or mobile UI is included this sprint.
- No email/SMS notifications (deferred to the backlog), so volunteers must check their personal roster view for assignments.
- The one-role rule is enforced per performance; cross-performance conflicts (e.g. the same volunteer on two simultaneous performances) are not checked.

## 5. Credentials, configuration and environment

- Local development requires Python 3.10+ and Git (see README "Prerequisites").
- No secrets are stored in the repository; a sample `.env.example` is provided for environment variables.
- Do not commit credentials or environment-specific configuration.

## 6. Recommended next-sprint backlog

- Strengthen validation (empty names, duplicate contact details).
- Add automated tests for the edge cases identified during acceptance testing.
- Consider a simple web UI for the coordinator and volunteers.
- Cross-performance conflict checking for the one-role rule.
- Track stories against Jira and record decisions in Confluence as required by the Definition of Done.
