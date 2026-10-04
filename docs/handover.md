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
