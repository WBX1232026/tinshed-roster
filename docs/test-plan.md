# Test Plan

> Owner: Yao Tingran (Business/Requirements Lead) & Li Qize (Technical Lead). Framework: pytest.

## 1. Scope and objectives

Verify that every acceptance criterion in `docs/acceptance-criteria.md` is met by the delivered application, and that the core one-role-per-performance rule holds on every create and update path.

## 2. Test approach and levels

| Level | What is verified | Where |
|---|---|---|
| Unit — validation | Blank names, malformed dates/times, invalid statuses, unknown ids | `tests/test_volunteer*.py`, `tests/test_production.py`, `tests/test_performance*.py`, `tests/test_assignment*.py` |
| Unit — store behaviour | Creation, sequential ids, find/update/deactivate, change/remove | same files |
| Rule tests | One-role rule: duplicate role rejected, different performance allowed, different volunteers allowed, rejected assignment not stored | `tests/test_one_role_rule.py` |
| View tests | Roster gap view (needed/assigned/open, overfill clamps at 0); personal view (own assignments only, chronological order) | `tests/test_roster_gap_view.py`, `tests/test_personal_view.py` |
| Integration — persistence | Seed CSV loading, SQLite snapshot round trip, id continuation after restore | `tests/test_persistence.py` |
| Acceptance | End-to-end walk-through of the three core scenarios | `tests/test_acceptance.py` |
| Regression | Smoke checks across all story areas after changes | `tests/test_regression.py` |
| Smoke | `python src/main.py` runs from a clean checkout | CI workflow step |

## 3. Entry and exit criteria

- **Entry:** code merged to `main`, tests import cleanly, `pip install -r requirements.txt` succeeds.
- **Exit:** full suite green (106 tests, 19 files), one-role rule covered by a dedicated file, CI green on Python 3.10 and 3.12.

## 4. Environment

- Python 3.10+ (developed on 3.12); SQLite (bundled); no external services.
- CI: GitHub Actions on every push to `main` and every pull request.

## 5. Test data

- Sample data: `data/sample_volunteers.csv`, `data/sample_productions.csv`.
- Fictional names only — no real member privacy is stored (see `docs/assumptions.md`).

## 6. Schedule and responsibilities

| Activity | Owner |
|---|---|
| Unit + rule + view + persistence tests | Li Qize |
| Acceptance + regression tests | Yao Tingran |
| CI configuration | Li Qize |
| UAT execution and record | Yao Tingran |

## 7. Risk and mitigation

- Risk: cross-performance conflicts not covered. Mitigation: recorded in Known issues and queued in next-sprint backlog.
