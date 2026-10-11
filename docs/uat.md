# User Acceptance Testing (UAT)

> Owner: Yao Tingran (Business/Requirements Lead). UAT confirms the delivered software meets the client's (The Tinshed Players Inc.) needs using realistic sample data.

## 1. UAT plan

- **Objective:** verify that Bec (volunteer coordinator) and Judith (producer) can perform the core rostering workflow without technical help.
- **Testers:** Yao Tingran (facilitating), with the three personas — Judith (producer), Bec (coordinator), Ravi (technical director) — represented.
- **Sample data:** 10 fictional volunteers loaded from `data/sample_volunteers.csv` and `data/sample_productions.csv` (no real member privacy).
- **Core scenarios:** three end-to-end flows (below), plus edge checks for the one-role rule and the two views.

### Sample volunteers (10)

| # | Name | Phone | Email |
|---|---|---|---|
| 1 | Col Hendricks | 0400 111 222 | col.h@example.com |
| 2 | Wendy Tran | 0400 222 333 | wendy.t@example.com |
| 3 | Marcus Webb | 0400 333 444 | marcus.w@example.com |
| 4 | Priya Nair | 0400 444 555 | priya.n@example.com |
| 5 | Sam O'Connor | 0400 555 666 | sam.o@example.com |
| 6 | Elena Rossi | 0400 666 777 | elena.r@example.com |
| 7 | Tom Nguyen | 0400 777 888 | tom.n@example.com |
| 8 | Grace Kim | 0400 888 999 | grace.k@example.com |
| 9 | Dylan Smith | 0400 999 000 | dylan.s@example.com |
| 10 | Aisha Bello | 0400 000 111 | aisha.b@example.com |

## 2. Core scenarios and results

### Scenario A — Build a full roster for a performance
1. Create production "The Weather House".
2. Add a Friday-evening performance with a crew call (Bar 1, Sound Op, Usher ×2).
3. Assign volunteers to each role; confirm one is left "unconfirmed".
4. Open the roster view.
**Result: PASS** — all roles shown, open positions marked, new assignments default to unconfirmed.

### Scenario B — One-role rule
1. Assign "Col Hendricks" to "Sound Op" for a performance.
2. Try to assign "Col Hendricks" to "Bar 1" for the same performance.
**Result: PASS** — the second assignment is refused with a reason naming the conflicting role; the store is unchanged.

### Scenario C — Personal roster view
1. Open the personal view for "Wendy Tran".
2. Confirm only her assignments appear, in date/time order, with production, date, start time and role.
3. Open the personal view for a volunteer with no assignments.
**Result: PASS** — own assignments only; empty list returned for a volunteer with none.

## 3. UAT sign-off

| Persona | Role | Outcome |
|---|---|---|
| Judith Ambrose | President / Producer | Accepts the season view and production/performance management |
| Bec Tanaka | Volunteer coordinator | Accepts roster building, one-role rule and gap view |
| Ravi Chandrasekaran | Technical director | Notes qualification matching as the top next-sprint item (PBI-1) |

**Overall UAT result: PASS.** The client accepts the delivered sprint scope; all deferred items are captured in the product backlog.
