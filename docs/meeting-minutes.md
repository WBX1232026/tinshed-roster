# Meeting Minutes

_Recorder: Yao Tingran (Business/Requirements Lead + Recorder)_

> Dates and attendance below are indicative — replace with the actual meeting dates and attendees for your team.

---

## Meeting 1 — Sprint Kick-off

**Date:** Sprint Week 0
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Requirements), Li Qize (Technical)

**Agenda**
1. Confirm project scope and division of work.
2. Agree the tooling and branch/PR workflow.
3. Assign roles and responsibilities.

**Discussion**
- Confirmed the sprint scope against the README: Volunteers, Productions/Performances, Crew Calls, Assignments, Views.
- Agreed to use GitHub with feature/documentation branches and pull-request review for every change.
- Agreed the Definition of Done: code committed on a named branch, acceptance criteria demonstrated, reviewed via PR, automated tests passing.

**Decisions**
- Scope is frozen to the five epics; out-of-scope items go to the product backlog.
- Every story gets a branch named for the story; no direct commits to `main`.

**Action items**
- [ ] Zhang Yixuan: project charter, Gantt chart, milestones.
- [ ] Yao Tingran: requirements analysis, scope, user stories with acceptance criteria.
- [ ] Li Qize: technical selection, data model, one-role rule, test strategy.

---

## Meeting 2 — Requirements Review

**Date:** Sprint Week 1
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Requirements), Li Qize (Technical)

**Agenda**
1. Walk through the user stories and acceptance criteria.
2. Resolve open questions on the one-role rule and persistence.

**Discussion**
- Reviewed US-1 to US-11 and confirmed the acceptance criteria are testable.
- Clarified that the one-role rule is per performance, not per production.
- Confirmed persistence requirement: a volunteer saved in one session must still exist after restart.

**Decisions**
- User stories and acceptance criteria approved as drafted in `docs/user-stories.md`.
- One-role rule applies to both create and move paths.

**Action items**
- [ ] Yao Tingran: push `docs/user-stories.md` and open a PR for review.
- [ ] Li Qize: implement the one-role rule with a test.

---

## Meeting 3 — Sprint Review / Handover

**Date:** Sprint Week 3
**Attendees:** Zhang Yixuan (PM), Yao Tingran (Requirements), Li Qize (Technical)

**Agenda**
1. Demo the delivered scope against the acceptance criteria.
2. Record acceptance testing results.
3. Agree the handover contents.

**Discussion**
- Demonstrated volunteer creation, one-role enforcement, and the roster gap view.
- Recorded acceptance testing results in `docs/acceptance-testing.md`.
- Agreed the six-part handover structure (delivered/not-delivered, run instructions, known issues, credentials, next-sprint backlog).

**Decisions**
- Sprint scope delivered; remaining items deferred to the product backlog.

**Action items**
- [ ] Yao Tingran: finalise `docs/handover.md` and open the acceptance-testing PR.
- [ ] Team: review and merge the documentation PRs.
