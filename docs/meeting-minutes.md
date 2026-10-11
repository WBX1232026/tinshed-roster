# Meeting Minutes

_Recorder: Yao Tingran (Business/Requirements Lead + Recorder)_

---

## Meeting 1 — Project Kickoff

**Date:** 2026-09-22
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Requirements), Li Qize (Technical)

**Agenda**
1. Align on the case requirements.
2. Agree the scope and division of work.
3. Agree tooling and the branch/PR workflow.

**Discussion**
- Confirmed the sprint scope: Volunteers, Productions/Performances, Crew Calls, Assignments, Views.
- Agreed to use GitHub with feature/documentation branches and pull-request review for every change.
- Confirmed the Definition of Done from the README.

**Decisions**
- Scope frozen to the five epics; out-of-scope items go to the product backlog.
- Every story gets a branch named for the story; no direct commits to `main`.

**Action items**
- [ ] Zhang Yixuan: project charter, Gantt chart, milestones.
- [ ] Yao Tingran: requirements analysis, scope, user stories with acceptance criteria.
- [ ] Li Qize: technical selection, data model, one-role rule, test strategy.

---

## Meeting 2 — Project Charter Approval

**Date:** 2026-09-23
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Requirements), Li Qize (Technical)

**Agenda**
1. Review the project charter.
2. Finalise scope, budget and constraints.

**Discussion**
- Reviewed the charter covering project objectives, scope, budget and constraints.
- Confirmed the client accepts either a Python CLI or a web application, with no additional requirements imposed.

**Decisions**
- Project charter approved.

**Action items**
- [ ] Zhang Yixuan: publish the approved charter and schedule.

---

## Meeting 3 — Requirements and Scope Approval

**Date:** 2026-09-25
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Requirements), Li Qize (Technical)

**Agenda**
1. Walk through the user stories and acceptance criteria.
2. Confirm exclusions and the backlog.
3. Resolve open questions on the one-role rule and persistence.

**Discussion**
- Reviewed US-1 to US-11 and confirmed the acceptance criteria are testable.
- Clarified that the one-role rule is per performance, not per production.
- Confirmed persistence: a volunteer saved in one session must still exist after restart.
- Recorded out-of-scope items in the product backlog (ticketing, membership fees, RSA/Blue Card matching, notifications, etc.).

**Decisions**
- Requirements and scope approved, as captured in `docs/user-stories.md` and `docs/requirements.md`.
- One-role rule applies to both create and move paths.

**Action items**
- [ ] Yao Tingran: push `docs/user-stories.md` and `docs/requirements.md`, open a PR for review.
- [ ] Li Qize: implement the one-role rule with a test.

---

## Meeting 4 — Design Approval

**Date:** 2026-09-30
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Requirements), Li Qize (Technical)

**Agenda**
1. Review the data model and architecture.
2. Confirm rules (one-role rule) and the persistence approach.

**Discussion**
- Reviewed the data model (volunteers, productions, performances, crew calls, assignments).
- Confirmed the one-role-per-performance rule is enforced on every create and update path.
- Confirmed sample data only; no real member privacy is stored.

**Decisions**
- Design approved (data model, rules, architecture).

**Action items**
- [ ] Li Qize: implement the agreed data model and rules.
- [ ] Yao Tingran: draft the acceptance testing record and handover document.

---

## Meeting 5 — Sprint 2 Planning

**Date:** 2026-10-01
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Sprint 2 PM), Li Qize (Technical)

**Agenda**
1. Review the Sprint 1 outcome.
2. Select the Sprint 2 backlog and set the sprint goal.

**Discussion**
- Sprint 1 delivered Volunteers, Productions/Performances, Crew Calls and Assignments.
- The two view stories (roster gap view, personal roster view) and validation hardening remain.

**Decisions**
- Sprint 2 goal: finish US-11 and US-12, and harden input validation.
- Yao Tingran takes the PM role for Sprint 2; QA/acceptance work assigned to Yao.

**Action items**
- [ ] Li Qize: implement US-11 and US-12, open PRs.
- [ ] Yao Tingran: draft test cases TR-T01–TR-T08 and the UAT plan.

---

## Meeting 6 — Daily Scrum

**Date:** 2026-10-08
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Sprint 2 PM), Li Qize (Technical)

**Updates**
- Li Qize: US-11 and US-12 implemented; PRs #16 and #17 open for review.
- Yao Tingran: test cases drafted; UAT scenarios defined.
- Zhang Yixuan: no blockers.

**Blockers**
- None.

---

## Meeting 7 — Sprint 2 Review

**Date:** 2026-10-11
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Sprint 2 PM), Li Qize (Technical)

**Agenda**
1. Demo the completed sprint work.
2. Gather client acceptance.

**Discussion**
- US-11 (roster gap view) and US-12 (personal roster view) demonstrated against the "Weather House" sample season.
- Client personas (Judith, Bec, Ravi) accepted both stories.

**Decisions**
- Both stories accepted; duplicate-email validation logged as TR-BUG-01 for the next sprint.

**Action items**
- [ ] Yao Tingran: record the review outcome and UAT results in `docs/uat.md`.

---

## Meeting 8 — Sprint 2 Retrospective

**Date:** 2026-10-11
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Sprint 2 PM), Li Qize (Technical)

**What went well**
- Clear Given/When/Then acceptance criteria kept scope tight.
- The two-layer architecture (store/service + web) kept the app testable (106 tests green).

**What to improve**
- Validation gaps (e.g. duplicate email) were found late — add a validation checklist to the Definition of Done.

**Actions**
- Add validation edge cases to the next-sprint backlog.
- Keep the 106-test suite green in CI.
