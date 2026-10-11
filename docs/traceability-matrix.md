# Traceability Matrix

> Owner: Yao Tingran (Business/Requirements Lead). Maps each user story to its functional requirement and to the tests that verify it.

| Story | Requirement | Test file(s) | Status |
|---|---|---|---|
| US-01 Create a volunteer record | FR-1, FR-2 | test_volunteer.py, test_volunteer_find_update.py | PASS |
| US-02 Find and update a volunteer | FR-3 | test_volunteer_find_update.py | PASS |
| US-03 Deactivate a volunteer | FR-4 | test_volunteer_deactivate.py | PASS |
| US-04 Create a production and performances | FR-5 | test_production.py, test_performance.py, test_performance_list.py | PASS |
| US-05 Change or remove a performance | FR-6 | test_performance.py, test_performance_list.py | PASS |
| US-06 Define a crew call | FR-7 | test_crew_call_define.py, test_crew_call_view.py | PASS |
| US-07 Assign a volunteer to a role | FR-8 | test_assignment.py | PASS |
| US-08 One-role rule | FR-9 | test_one_role_rule.py, test_store_one_role_rule.py | PASS |
| US-09 Change or remove an assignment | FR-10 | test_assignment_change_remove.py | PASS |
| US-10 Track confirmed/notified separately | FR-11 | test_assignment.py | PASS |
| US-11 Roster gap view | FR-12 | test_roster_gap_view.py, test_web_roster.py | PASS |
| US-12 Personal roster view | FR-13 | test_personal_view.py, test_web_personal.py | PASS |
| — Persistence across restarts | FR-2 (NFR) | test_persistence.py | PASS |

> Functional requirement IDs (FR-1 … FR-13) are defined in `docs/requirements.md`. Every story has at least one automated test; every test file is green in CI.
