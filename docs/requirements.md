# Requirements Analysis and Scope Definition

## 1. Project Overview

Tinshed Roster is a show scheduling and volunteer crew rostering system for The Tinshed Players Inc., a community theatre company based at the Wynnum School of Arts Hall, Queensland. The company has staged plays continuously since 1998, with a maximum of four productions per year and eight performances per production (Friday evening, Saturday matinee, Saturday evening, Sunday matinee across two weekends).

Volunteer rostering currently depends on a Facebook group, group texts, an exercise book, and the coordinator's personal notebook, causing duplicate assignments, unfilled roles, inconsistent versions, and phone calls asking who is on.

**Vision:** one place that holds the season's productions, their performances, and who is crewing each one — letting the coordinator build a roster and see where the holes are, and letting a volunteer see what they have been put down for without asking anyone.

## 2. Stakeholders and Roles

| Stakeholder | Role | Primary concern |
|---|---|---|
| Judith Ambrose | President / Producer | The season: which show is on, is the hall free, is the committee on board. She wants to stop being phoned at home with questions she cannot answer. |
| Bec Tanaka | Volunteer coordinator | The roster itself: who is on, who has confirmed, where the holes are. The heaviest user of the software. |
| Ravi Chandrasekaran | Technical director | Capability and risk: very few people can work the lights/sound desks; he wants a trained-operators list that lives outside his head. |

## 3. Functional Requirements

| ID | Requirement | Story |
|---|---|---|
| FR-1 | Create a volunteer with at least a name and a way to contact them | US-1 |
| FR-2 | Persist volunteers across application restarts | US-1 |
| FR-3 | Find a volunteer by name and update name, phone, or email | US-2 |
| FR-4 | Deactivate a volunteer without losing existing assignments | US-3 |
| FR-5 | Create a production and add performances with date and start time; list them in order | US-4 |
| FR-6 | Change or remove a performance without affecting others | US-5 |
| FR-7 | Define a per-performance crew call: roles, number needed, and call times (crew 60 min, FOH/box office 45 min before curtain); calls differ between evening and matinee | US-6 |
| FR-8 | Assign a volunteer to a role for a performance; new assignments default to "unconfirmed" | US-7 |
| FR-9 | Enforce the one-role rule: at most one role per volunteer per performance, refused with a reason, on both create and move | US-8 |
| FR-10 | Change or remove an assignment; removal leaves the position open | US-9 |
| FR-11 | Track "confirmed" and "notified" as two separate flags on an assignment | US-10 |
| FR-12 | Roster view showing filled and open positions | US-11 |
| FR-13 | Personal roster view listing a volunteer's own assignments | US-12 |

## 4. Non-functional Requirements

- **Persistence:** data written in one session survives an application restart.
- **Consistency:** the one-role rule is enforced on every create and update path, including moving an existing assignment.
- **Usability:** simple, text-driven interface suitable for a non-technical volunteer coordinator.
- **Testability:** automated tests (pytest) cover the story behaviours, including at least one test of the one-role-per-performance rule.

## 5. In Scope (this sprint)

- Volunteers: create, find, update, deactivate.
- Productions and performances: create, update, delete; performances carry a date and start time.
- Per-performance crew call: roles, number needed, and call times; calls differ between evening and matinee.
- Assignments: create, change, delete; new assignments default to "unconfirmed"; "confirmed" and "notified" tracked separately.
- One-role rule: a volunteer may hold at most one role in the same performance.
- Views: performance/production roster (filled and open positions); volunteer's personal roster.

## 6. Out of Scope (deferred to product backlog)

The following are all things Judith, Bec or Ravi asked for. They are recorded, prioritised and parked in the product backlog (see `docs/user-stories.md`, PBI-1 to PBI-12), not delivered this sprint:

- Skill / qualification matching (who is trained on lights or sound) — PBI-1
- Volunteer unavailable dates — PBI-2
- RSA / Blue Card recording and matching — PBI-3
- Minimum-two-ushers fire-regulation rule — PBI-4
- Volunteer shift swaps — PBI-5
- Email / SMS reminders — PBI-6
- Equipment inventory — PBI-7
- Emergency contact, membership number, T-shirt size — PBI-8
- Membership fees and renewals — PBI-9
- Ticketing and box-office sales (TicketNest) — PBI-10
- Volunteer hours reporting and grant acquittal — PBI-11
- Venue booking clash detection — PBI-12

## 7. Assumptions and Dependencies

- A production runs eight performances across two weekends, but performances are entered individually with their own date and start time.
- Contact details are free text; no external messaging integration this sprint.
- The one-role rule applies per performance, not per production — the same volunteer may hold different roles on different performances.
- Crew call times follow the company's standing practice (crew 60 min, FOH/box office 45 min before curtain).
