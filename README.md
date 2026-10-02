# Tinshed Roster

Show scheduling and volunteer crew rostering system for The Tinshed Players Inc.

## Project Background

The Tinshed Players Inc. is a community theatre company based at the Wynnum School of Arts Hall, 84 Rowan Street, Wynnum, Queensland. It has staged plays continuously since 1998, with a maximum of four productions per year. Each production runs eight performances across two weekends: Friday evening, Saturday matinee, Saturday evening, and Sunday matinee.

Volunteer rostering currently depends on a Facebook group, group texts, an exercise book, and the coordinator's personal notebook. This has caused duplicate assignments, unfilled roles, inconsistent versions, and phone calls asking who is on.

## Project Vision

One place that holds the season's productions, their performances, and who is crewing each one. The software should let the coordinator build a roster and see at a glance where the holes are, and let a volunteer see what they have been put down for without asking anyone.

## Scope (Sprint)

- Volunteers: create, find, update, deactivate
- Productions and performances: create, update, delete; performances have date and start time
- Per-performance crew call: roles and number needed
- Assignments: create, change, delete; new assignments default to "unconfirmed"
- One-role rule: a volunteer may hold at most one role in the same performance
- Views: performance/production roster showing filled and open positions; volunteers can see their own assignments

## Out of Scope

Ticketing and box office sales, membership fees and renewals, RSA/Blue Card/qualification matching, rehearsals and casting, venue booking clashes, grant acquittal, equipment inventory, email/SMS notifications, volunteer shift swaps, hours reporting, TicketNest integration.

All of the above go into the product backlog and are not part of this sprint.

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
python src/main.py
```

## Running the tests

```bash
pytest
```

## Project structure

```text
tinshed-roster/
├── src/          # application code
├── tests/        # automated tests
├── data/         # sample data
├── docs/         # assumptions and decisions
├── requirements.txt
├── .gitignore
└── README.md
```

## Definition of Done

- Code committed and pushed to GitHub, on a branch named for the story
- Every acceptance criterion met and demonstrated against the story in Jira
- Reviewed by another team member through a pull request; comments addressed before merging
- Automated tests covering the story's behaviour exist and pass, including at least one test of the one-role-per-performance rule
- Application runs from a clean checkout by following this README alone
- No known critical defects: nothing that loses an assignment, accepts a roster the rule forbids, or stops the application starting
- Jira issue updated to reflect the true state of the work; decisions and assumptions recorded in Confluence

## Team

| Member | Role | Responsibilities |
|---|---|---|
| Zhang Yixuan | Project Manager + Schedule/Roster Lead | Overall progress, chairing meetings, charter, Gantt chart, milestones |
| Yao Tingran | Business/Requirements Lead + Recorder | Requirements analysis, scope, user stories, meeting minutes, Confluence handover |
| Li Qize | Technical Lead + Feasibility/WBS | Technical selection, data model, one-role rule, test strategy, deployment instructions |
