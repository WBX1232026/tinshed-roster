# Test Results

> Owner: Yao Tingran (Business/Requirements Lead). Suite: **106 tests, 19 test files, all passing**.

## Summary

| Metric | Value |
|---|---|
| Total tests | 106 |
| Passed | 106 |
| Failed | 0 |
| Test files | 19 |

## Results by file

| Test file | Tests | Result |
|---|---|---|
| test_crew_call_define.py | 9 | PASS |
| test_volunteer_find_update.py | 8 | PASS |
| test_assignment_change_remove.py | 8 | PASS |
| test_assignment.py | 8 | PASS |
| test_roster_gap_view.py | 7 | PASS |
| test_regression.py | 7 | PASS |
| test_volunteer_deactivate.py | 6 | PASS |
| test_volunteer.py | 6 | PASS |
| test_store_one_role_rule.py | 6 | PASS |
| test_production.py | 6 | PASS |
| test_performance.py | 6 | PASS |
| test_personal_view.py | 5 | PASS |
| test_persistence.py | 5 | PASS |
| test_performance_list.py | 4 | PASS |
| test_crew_call_view.py | 4 | PASS |
| test_web_personal.py | 3 | PASS |
| test_one_role_rule.py | 3 | PASS |
| test_acceptance.py | 3 | PASS |
| test_web_roster.py | 2 | PASS |

## How to reproduce

```bash
git clone https://github.com/WBX1232026/tinshed-roster.git
cd tinshed-roster
pip install -r requirements.txt
pytest -q          # -> 106 passed
```

## Core rule coverage

`test_one_role_rule.py` and `test_store_one_role_rule.py` together prove the one-role rule: duplicate role rejected, the same role twice rejected, different performances allowed, different volunteers allowed, the violation message names the conflicting role, and a rejected assignment leaves the store unchanged.

## CI status

`.github/workflows/ci.yml` runs the full suite plus a `python src/main.py` smoke step on Python 3.10 and 3.12 for every push to `main` and every pull request.
