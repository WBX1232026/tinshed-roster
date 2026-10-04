# Handover Document

## 1. What was delivered against scope

| Capability | Jira Story | Status |
|---|---|---|
| Volunteer records | US-1, US-2, US-3 | Delivered |
| Productions and performances | US-4, US-5 | Delivered |
| Per-performance crew call | US-6 | Delivered |
| Assignments | US-7, US-9 | Delivered |
| One-role rule | US-8 | Delivered |
| Roster gap view | US-10 | Delivered |
| Personal roster view | US-11 | Delivered |

## 2. What was not delivered, and why

The following items were requested by stakeholders but are out of scope for this sprint. They remain in the product backlog.

| Item | Reason | Backlog location |
|---|---|---|
| Ticketing and box office sales | Out of scope | Product backlog |
| Membership fees and renewals | Out of scope | Product backlog |
| RSA/Blue Card/qualification matching | Out of scope | Product backlog |
| Rehearsals and casting | Out of scope | Product backlog |
| Venue booking clashes | Out of scope | Product backlog |
| Grant acquittal | Out of scope | Product backlog |
| Equipment inventory | Out of scope | Product backlog |
| Email/SMS notifications | Out of scope | Product backlog |
| Volunteer shift swaps | Out of scope | Product backlog |
| Hours reporting | Out of scope | Product backlog |
| TicketNest integration | Out of scope | Product backlog |

## 3. Setup and run instructions from GitHub

1. Clone the repository:
   git clone https://github.com/WBX1232026/tinshed-roster.git
   cd tinshed-roster
2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run the application:
   python -m flask --app src.app run
5. Open http://127.0.0.1:5000 in your browser.
6. Run the tests:
   pytest

## 4. Known issues and limitations

- Data is stored in memory or SQLite; no multi-user concurrency.
- No authentication or roles.
- No deployment to a public server.
- Only sample data is used; no real member privacy data.

## 5. Credentials, configuration and environment

- `.env.example` contains sample configuration.
- No real credentials are stored.
- Sample data is in `data/sample_volunteers.csv` and `data/sample_productions.csv`.

## 6. Recommended next-sprint backlog

| Priority | Item | Reason |
|---|---|---|
| 1 | Persist data in SQLite | Needed for real use |
| 2 | Add login and roles | Only the coordinator should manage the roster |
| 3 | Add email or SMS notification | Reduce phone calls |
| 4 | Add shift swap feature | Reduce coordinator workload |
| 5 | Add hours reporting | Support grant acquittal |
| 6 | Add ticketing integration | Single place for the season |
| 7 | Add membership renewals | Reduce admin |
| 8 | Add RSA/Blue Card tracking | Compliance |
| 9 | Add equipment inventory | Support grant applications |
| 10 | Add public roster view | Volunteers can check without logging in |
