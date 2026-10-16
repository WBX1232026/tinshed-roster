# Technical Guide

Owner: Li Qize (Technical Lead)
Audience: the next maintainer / tutor marking this repository.

## Getting started in five minutes

```bash
git clone https://github.com/WBX1232026/tinshed-roster.git
cd tinshed-roster
python -m venv venv
venv\Scripts\activate          # Windows (source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python data/seed.py            # optional: write the sample season to the database
python -m flask --app src.app run
# open http://127.0.0.1:5000
```

The full test suite should pass from a clean checkout:

```bash
pytest
# 102 passed
```

## Repository layout

| Path | Contents |
|---|---|
| `src/` | Application code (views, stores, persistence, models, errors) |
| `templates/` | Jinja2 HTML templates (base + one per view) |
| `tests/` | Automated tests (one file per feature area) |
| `data/` | CSV sample data + `seed.py` loader |
| `deploy/` | Deployment script (`deploy.sh`) |
| `docs/` | Project documentation (this guide, architecture, data model, ...) |
| `.github/workflows/ci.yml` | CI: installs dependencies and runs pytest on push/PR |

## Domain stores

Each entity has one store class in `src/`:

| Store | File | Key operations |
|---|---|---|
| `VolunteerStore` | `src/volunteer.py` | create, find, find_all, find_by_name, update, deactivate |
| `ProductionStore` | `src/production.py` | create, find, find_all, update |
| `PerformanceStore` | `src/performance.py` | create, find, find_all, update, remove |
| `CrewCallStore` | `src/crew_call.py` | define/update a crew call, list roles |
| `AssignmentStore` | `src/assignment.py` | create, find, update, remove; enforces the one-role rule |

All stores follow the same conventions:

- `create` validates input and raises `ValidationError` for bad data.
- `find` raises `NotFoundError` for unknown ids.
- Business rules raise `RuleViolationError`.
- Stores are in-memory dicts; `src/database.py` snapshots them to SQLite.

## Adding a new feature

1. Add the logic to the relevant store (or a new store module).
2. Expose it in `src/views.py` (new route on the `views` blueprint) and add a
   template in `templates/`.
3. Add tests in `tests/` — one file per feature area, importing directly from
   `src.*` (the root `conftest.py` guarantees `sys.path`).
4. Run `pytest`; CI runs the same command on every push and PR.

## Testing conventions

- Unit tests hit the stores directly (no web server, no database file).
- Web tests use Flask's test client and follow each route's happy path and
  error paths (400/404/409).
- The one-role rule has its own dedicated suites: `tests/test_one_role_rule.py`
  and `tests/test_store_one_role_rule.py`.
- Acceptance and regression suites live in `tests/test_acceptance.py` and
  `tests/test_regression.py` (added in PR #24).

## Error reference

| Exception | HTTP | Example |
|---|---|---|
| `ValidationError` | 400 | Blank volunteer name |
| `NotFoundError` | 404 | Unknown volunteer id |
| `RuleViolationError` | 409 | Second role for the same volunteer in one performance |

## Configuration (environment variables)

| Variable | Default | Meaning |
|---|---|---|
| `DATABASE_URL` | `sqlite:///data/tinshed_roster.db` | Where the SQLite snapshot lives |
| `SEED_DATA` | `true` | Load CSV seed data when no database exists |

See `.env.example` — it contains placeholders only; no real secrets are ever
committed to the repository.
