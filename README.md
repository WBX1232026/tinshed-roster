# Tinshed Roster

Show scheduling and volunteer crew rostering system for The Tinshed Players Inc.

## Prerequisites

- Python 3.10+
- Git

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/WBX1232026/tinshed-roster.git
   cd tinshed-roster
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the application

```bash
python -m flask --app src.app run
```

Open http://127.0.0.1:5000 in your browser.

To see the sample season, load the seed data first:

```bash
python data/seed.py
```

## Running the tests

```bash
pytest
```

## Scope

- Volunteers
- Productions and performances
- Per-performance crew call
- Assignments (including the one-role rule)
- Roster gap view
- Personal roster view

## Out of scope

Ticketing, membership fees, RSA/Blue Card matching, rehearsals and casting, venue booking clashes, grant acquittal, equipment inventory, email/SMS, shift swaps, hours reporting, TicketNest integration.
