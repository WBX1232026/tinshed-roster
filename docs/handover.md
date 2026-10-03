# Handover Document

## 1. What was delivered against scope

- **Volunteers** (US-1, US-2, US-3): create, find, update and deactivate a volunteer; deactivation preserves existing assignments.
- **Productions and performances** (US-4, US-5): create a production, add/change/remove performances, list them in date and time order.
- **Crew calls** (US-6): record roles and the number needed per performance.
- **Assignments** (US-7, US-8, US-9): assign, change and remove assignments; new assignments default to "unconfirmed"; the one-role-per-performance rule is enforced.
- **Views** (US-10, US-11): roster view showing filled and open positions; personal roster view listing a volunteer's own assignments.
- **Requirements artefacts**: user stories with acceptance criteria (see `docs/user-stories.md`) and an acceptance testing record (see `docs/acceptance-testing.md`).

## 2. What was not delivered, and why

- Out-of-scope items listed in the README (ticketing, membership fees, RSA/Blue Card matching, rehearsals and casting, venue booking clashes, grant acquittal, equipment inventory, email/SMS notifications, shift swaps, hours reporting, TicketNest integration) remain in the product backlog and were not part of this sprint.
- (Fill in any sprint items that slipped, with the reason — e.g. time constraints or dependency on another story.)

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

- (Fill in as applicable — e.g. validation gaps such as empty names or duplicate phone numbers, or any edge cases not yet covered.)

## 5. Credentials, configuration and environment

- Local development requires Python 3.10+ and Git (see README "Prerequisites").
- No secrets are stored in the repository; a sample `.env.example` is provided for environment variables.
- Do not commit credentials or environment-specific configuration.

## 6. Recommended next-sprint backlog

- Strengthen validation (empty names, duplicate contact details).
- Add automated tests for edge cases identified during acceptance testing.
- Track stories against Jira and record decisions in Confluence as required by the Definition of Done.
