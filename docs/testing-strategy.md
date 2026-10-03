# Testing Strategy

Owner: Li Qize (Technical Lead)
Framework: pytest. Suite: 88 tests, 14 test files, `tests/` directory.

## Goals

1. Every acceptance criterion has at least one automated test.
2. The one-role-per-performance rule is covered by a dedicated test file.
3. The suite runs from a clean checkout (`pip install -r requirements.txt && pytest`) and inside CI in under 5 minutes.

## Test layers

| Layer | What is tested | Files |
|---|---|---|
| Unit - validation | Blank names, malformed dates/times, invalid statuses, unknown ids | `test_volunteer*.py`, `test_production.py`, `test_performance*.py`, `test_assignment*.py` |
| Unit - store behaviour | Creation, sequential ids, find/update/deactivate, change/remove | same files |
| Rule tests | The one-role rule: duplicate role rejected, different performance allowed, different volunteers allowed, rejected assignment not stored | `test_one_role_rule.py` |
| View tests | Roster gap view (needed/assigned/open, overfill clamps at 0) and personal view (own assignments only, chronological order) | `test_roster_gap_view.py`, `test_personal_view.py` |
| Integration - persistence | Seed CSV loading, SQLite snapshot round trip, id continuation after restore | `test_persistence.py` |
| Smoke | `python src/main.py` runs from a clean checkout | CI workflow step |

## Core rule coverage

`tests/test_one_role_rule.py` contains six tests proving:

- a volunteer cannot hold two roles in the same performance,
- the same role twice is also rejected,
- the same volunteer can be assigned to **different** performances,
- two volunteers can share a performance,
- the violation message names the conflicting role,
- a rejected assignment leaves the store unchanged.

## Conventions

- One test file per story area; fixtures (`store`, `stores`, `service`) set up fresh stores per test, so tests never share state.
- Tests assert behaviour through the public store API, not internal fields.
- `conftest.py` at the project root puts the root on `sys.path`, so tests import with `from src.xxx import ...`.

## Running the tests

```bash
pip install -r requirements.txt
pytest            # full suite
pytest tests/test_one_role_rule.py   # just the core rule
```

## CI

`.github/workflows/ci.yml` runs `pytest` plus a `python src/main.py` smoke step on Python 3.10 and 3.12 for every push to `main` and every pull request. A failing run blocks the merge review.
