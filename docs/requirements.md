# Requirements Analysis and Scope Definition

## 1. Project Overview

Tinshed Roster is a show scheduling and volunteer crew rostering system for The Tinshed Players Inc., a community theatre company based at the Wynnum School of Arts Hall, Queensland. The company has staged plays continuously since 1998, with a maximum of four productions per year and eight performances per production (Friday evening, Saturday matinee, Saturday evening, Sunday matinee across two weekends).

Volunteer rostering currently depends on a Facebook group, group texts, an exercise book, and the coordinator's personal notebook, causing duplicate assignments, unfilled roles, inconsistent versions, and phone calls asking who is on.

**Vision:** one place that holds the season's productions, their performances, and who is crewing each one — letting the coordinator build a roster and see where the holes are, and letting a volunteer see what they have been put down for without asking anyone.

## 2. Stakeholders and Roles

| Role | Responsibility |
|---|---|
| Volunteer coordinator | Build and maintain the roster; manage volunteers and assignments |
| Producer | Create productions and their performances |
| Volunteer | View the performances they are rostered on |

## 3. Functional Requirements

| ID | Requirement |
|---|---|
| FR-1 | Create a volunteer with at least a name and a way to contact them (US-1) |
| FR-2 | Persist volunteers across application restarts (US-1) |
| FR-3 | Find a volunteer by name and update name, phone, or email (US-2) |
| FR-4 | Deactivate a volunteer without losing existing assignments (US-3) |
| FR-5 | Create a production and add performances with date and start time (US-4) |
| FR-6 | Change or remove a performance without affecting others (US-5) |
| FR-7 | Define a crew call (roles and number needed) per performance (US-6) |
| FR-8 | Assign a volunteer to a role for a performance; new assignments default to "unconfirmed" (US-7) |
| FR-9 | Enforce the one-role rule: at most one role per volunteer per performance (US-8) |
| FR-10 | Change or remove an assignment (US-9) |
| FR-11 | Roster view showing filled and open positions (US-10) |
| FR-12 | Personal roster view listing a volunteer's own assignments (US-11) |

## 4. Non-functional Requirements

- **Persistence:** data written in one session survives an application restart.
- **Consistency:** the one-role rule is enforced on every create and update path, including moving an existing assignment.
- **Usability:** simple, text-driven interface suitable for a non-technical volunteer coordinator.
- **Testability:** automated tests (pytest) cover the story behaviours, including at least one test of the one-role-per-performance rule.

## 5. In Scope (this sprint)

- Volunteers: create, find, update, deactivate.
- Productions and performances: create, update, delete; performances carry a date and start time.
- Per-performance crew call: roles and number needed.
- Assignments: create, change, delete; new assignments default to "unconfirmed".
- One-role rule: a volunteer may hold at most one role in the same performance.
- Views: performance/production roster (filled and open positions); volunteer's personal roster.

## 6. Out of Scope (deferred to product backlog)

Ticketing and box office sales, membership fees and renewals, RSA/Blue Card/qualification matching, rehearsals and casting, venue booking clashes, grant acquittal, equipment inventory, email/SMS notifications, volunteer shift swaps, hours reporting, TicketNest integration.

## 7. Assumptions and Dependencies

- A production runs eight performances across two weekends by default, but performances are entered individually with their own date and start time.
- Contact details (phone/email) are treated as free text; no external messaging integration is required this sprint.
- The one-role rule applies per performance, not per production — the same volunteer may hold different roles on different performances.
