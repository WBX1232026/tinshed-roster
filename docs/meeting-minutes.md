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
