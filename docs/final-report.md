# Final Project Report — Tinshed Roster

**Unit:** ISYS3001 Managing Software Development — Assessment 3 (Report)
**Weight:** 50%
**Team:** Zhang Yixuan (Project Manager), Yao Tingran (Business/Requirements Lead + Recorder), Li Qize (Technical Lead)
**Date:** 12 October 2026
**Submission:** Group

> **Formatting note (apply in Word):** 12 pt Arial, 1.5 line spacing, APA 7th referencing.

---

## Academic Integrity Declaration

By submitting this assessment, I declare that I have read and understood SCU's Academic Integrity policies and referencing guidelines. I am aware of the consequences of academic misconduct and confirm that this submission is my own original work, referenced appropriately, and has not been previously submitted. I authorise its reproduction for authentication purposes and understand the implications of a false declaration. I have adhered to guidelines regarding Generative AI.

---

## Executive Summary

This report documents how a three-person team applied the Scrum framework to deliver **Tinshed Roster**, a show-scheduling and volunteer-crewing web application for The Tinshed Players Inc., a community theatre company. The project ran from 22 September to 12 October 2026 across two sprints. Sprint 1 delivered the volunteer, production, crew-call and assignment epics; Sprint 2 delivered the two view stories and hardened input validation. The product backlog contained twelve user stories (40 story points) across five epics, with a further twelve items deferred to a prioritised backlog. The team used Jira for backlog, sprint and test management, GitHub for source control with pull-request review, and a pytest suite of 106 tests across 19 files, all passing. User acceptance testing passed all three core scenarios, and the three client personas formally accepted the delivered scope. This report summarises the process, outcomes and lessons learned, and documents each member's individual contribution.

---

## 1. Introduction

### 1.1 Project background

The Tinshed Players Inc. is a community theatre company based at the Wynnum School of Arts Hall, Queensland, staging up to four productions a year with eight performances each. Volunteer rostering currently relies on a Facebook group, group texts, an exercise book and the coordinator's notebook, which produces duplicate assignments, unfilled roles, inconsistent versions and constant phone calls. The project's goal was a single web application that holds the season's productions, their performances, and who is crewing each one — letting the coordinator build a roster and see the gaps, and letting a volunteer see their own assignments.

### 1.2 Team and roles

| Member | Primary role | PM rotation |
|---|---|---|
| Zhang Yixuan | Project Manager (Sprint 1 PM) | Sprint 1 |
| Yao Tingran | Business/Requirements Lead, Recorder, QA | Sprint 2 |
| Li Qize | Technical Lead | — |

Each member took a turn as project manager, satisfying the rotation requirement.

### 1.3 Report structure

Section 2 covers initiation and planning; Section 3 details the Scrum process; Section 4 summarises outcomes and performance; Section 5 draws lessons learned; Section 6 highlights individual contribution by colour; Section 7 records formal acceptance.

---

## 2. Project Initiation and Planning

The team formalised scope, roles and tooling in the project charter (approved at the meeting of 23 September 2026). The charter fixed the vision, the five-epic scope (Volunteers, Productions, Assignments, Views), the budget (zero-cost, open-source tooling only), and the constraints.

Key planning decisions, recorded in Jira and in the meeting minutes:

- **Scope** was frozen to five epics; every out-of-scope request was parked in the product backlog rather than dropped.
- **Tooling** was agreed: Jira for backlog/sprint/test management, GitHub with a branch-and-pull-request workflow for every change, and pytest for automated testing.
- **Definition of Done** was confirmed from the repository README: a story is done only when it is implemented, tested, and merged via a reviewed pull request.
- **Role rotation** was agreed so that each member leads one sprint as project manager.

The technical lead documented the technology selection (Python 3.10+, Flask, SQLite, pytest, GitHub Actions, Docker) and the data model, which were reviewed and approved at the design meeting of 30 September 2026.

---

## 3. The Scrum Process

### 3.1 Product backlog

The product backlog, maintained in Jira and mirrored in `docs/product-backlog.md`, contained twelve user stories grouped into five epics. Every story carried a user-role narrative, Given/When/Then acceptance criteria, a story-point estimate and a priority.

| Epic | Stories | Story points |
|---|---|---|
| Volunteers | US-01–US-03 | 8 |
| Productions | US-04–US-06 | 13 |
| Assignments | US-07–US-10 | 13 |
| Views | US-11–US-12 | 6 |
| **Total** | **12** | **40** |

A further twelve product backlog items (PBI-1 to PBI-12) — such as skill/qualification matching, shift swaps and reminders — were recorded, prioritised and deferred, keeping the sprint scope realistic.

### 3.2 Sprint planning and backlogs

Two sprints were planned. **Sprint 1** (22–30 September) committed the Volunteers, Productions and Assignments epics. **Sprint 2** (1–11 October) committed the two view stories (US-11 roster gap view, US-12 personal roster view) plus validation hardening, with the sprint goal "finish the two view stories and harden input validation". Yao Tingran took the project-manager role for Sprint 2.

### 3.3 Execution and daily scrums

Development followed the branch-and-pull-request workflow agreed at kickoff — one branch per story, no direct commits to `main`. The technical lead implemented the stories and opened pull requests for review; the daily scrum of 8 October recorded US-11 and US-12 as implemented (PRs #16 and #17) with no blockers.

### 3.4 Test plan and results

The test plan (`docs/test-plan.md`) defined eight test cases (TR-T01 to TR-T08) covering volunteer creation, the one-role rule, the roster gap view, the personal view, browser compatibility and the acceptance test. The full pytest suite ran **106 tests across 19 files, all passing**, with the one-role rule proven on both create and move paths. Continuous integration (GitHub Actions) runs the suite plus a smoke test on every push and pull request.

### 3.5 Configuration, change and release management

Source code and configuration were version-controlled in GitHub with pull-request review as the change-control gate. Releases were managed through tagged commits and a `CHANGELOG.md`. Procurement and feasibility were addressed in the companion documents (technology selection and procurement plan) from Assessment 2, confirming all components are open source with zero licensing cost.

### 3.6 Sprint review and retrospective

At the Sprint 2 review (11 October), the two view stories were demonstrated against the "Weather House" sample season and accepted by the three client personas. A duplicate-email validation gap was logged as TR-BUG-01 for the next sprint. The retrospective (same day) recorded two strengths — clear Given/When/Then criteria kept scope tight, and the two-layer architecture kept the app testable — and one improvement: add a validation checklist to the Definition of Done.

---

## 4. Project Outcomes and Performance

The project delivered all twelve committed stories. The final application lets the coordinator create and maintain volunteers, productions and performances, define per-performance crew calls, enforce the one-role rule, and see the roster gap view and each volunteer's personal view. User acceptance testing (`docs/uat.md`) passed all three core scenarios against ten sample volunteers, and Judith (producer), Bec (coordinator) and Ravi (technical director) each accepted the delivered scope. The 106-test suite remained green throughout. The one known defect (duplicate email) was captured, prioritised and deferred to the next sprint, which is consistent with disciplined backlog management.

---

## 5. Lessons Learned

Three lessons emerged:

1. **Testable acceptance criteria are the highest-leverage artefact.** Writing every story as Given/When/Then made scope unambiguous and let the QA role turn criteria directly into pytest cases, which is why 106 tests map cleanly onto the twelve stories.
2. **A two-layer architecture pays for itself.** Separating the store/service layer from the web layer kept business rules unit-testable and the web views thin, which surfaced the one-role rule and the view logic as small, testable units.
3. **Validation should be defined up front, not discovered in review.** The duplicate-email gap was found late because validation edge cases were not part of the Definition of Done; adding a validation checklist is the concrete corrective action for the next sprint.

---

## 6. Individual Contributions

The following contributions are highlighted in colour by team member, as required.

> **Colour legend (apply in Word):** <span style="color:#2B579A">**Blue — Yao Tingran**</span> · <span style="color:#217346">**Green — Li Qize**</span> · <span style="color:#C55A11">**Orange — Zhang Yixuan**</span>

| Area | Contribution |
|---|---|
| Requirements & scope | <span style="color:#2B579A">Yao Tingran</span> wrote the requirements analysis, scope definition and user stories with acceptance criteria. |
| User stories & backlog | <span style="color:#2B579A">Yao Tingran</span> authored US-01 to US-12 and the twelve deferred PBIs, with story points and priorities. |
| Testing & QA | <span style="color:#2B579A">Yao Tingran</span> defined the test plan, test cases TR-T01–TR-T08, the traceability matrix, and the UAT plan and results. |
| Recorder | <span style="color:#2B579A">Yao Tingran</span> recorded all meeting minutes and drove the retrospective. |
| Technical design | <span style="color:#217346">Li Qize</span> selected the technology stack and designed the data model and architecture. |
| Implementation | <span style="color:#217346">Li Qize</span> implemented the store/service and web layers, including the one-role rule and the two views. |
| Testing (code) | <span style="color:#217346">Li Qize</span> built the pytest suite and CI workflow (106 tests green). |
| Project management | <span style="color:#C55A11">Zhang Yixuan</span> produced the project charter, Gantt chart and milestones, and led Sprint 1 as PM. |
| Release management | <span style="color:#C55A11">Zhang Yixuan</span> managed branches, pull requests, releases and the CHANGELOG. |

---

## 7. Formal Acceptance

The delivered scope was formally accepted at the Sprint 2 review meeting on 11 October 2026. The three client personas — Judith Ambrose (President/Producer), Bec Tanaka (Volunteer Coordinator) and Ravi Chandrasekaran (Technical Director) — each accepted the delivered sprint scope, with qualification matching (PBI-1) noted as the top next-sprint item. Formal acceptance from the lecturer and tutor will be obtained at the 10-minute presentation and 5-minute question-and-answer session.

---

## References

- Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide*. Scrum.org. https://scrumguides.org/scrum-guide.html
- Atlassian. (n.d.). *Jira Software — Scrum boards*. https://www.atlassian.com/software/jira
- Pallets Projects. (n.d.). *Flask — web development, one drop at a time*. https://flask.palletsprojects.com/
- Holscher, B. (n.d.). *pytest — helps you write better programs*. https://docs.pytest.org/

---

## Appendix — Deliverables index

| Deliverable | Location |
|---|---|
| Project charter | (team artefact, Jira) |
| Product backlog | `docs/product-backlog.md` + Jira |
| Meeting memos | `docs/meeting-minutes.md` + Jira |
| Test plan & results | `docs/test-plan.md`, `docs/test-results.md` + Jira |
| UAT | `docs/uat.md` |
| Traceability matrix | `docs/traceability-matrix.md` |
| Source code | GitHub — https://github.com/WBX1232026/tinshed-roster |
| Peer evaluation | Blackboard (individual, confidential) |
