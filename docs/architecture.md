# Architecture

Owner: Li Qize (Technical Lead)
Related documents: `docs/tech-stack.md`, `docs/data-model.md`, `docs/one-role-rule.md`

## Overview

Tinshed Roster is a layered Flask application: web views talk to in-memory
stores, and persistence is a thin snapshot layer underneath. The whole app is
small enough to run from a single command and stores its data in one SQLite
file, so no database server is ever needed.

## Layers

```
templates/ (Jinja2 HTML)
      |
      v
src/views.py            # Flask blueprint: routes + request handling
      |
      v
src/*.py stores         # domain logic: volunteer, production, performance,
                        # crew_call, assignment (+ roster.py, personal.py views)
      |
      v
src/database.py         # SQLite snapshot load/save
src/storage.py          # CSV seed import
src/models.py           # dataclasses shared by stores and database
```

- **Views** (`src/views.py`, blueprint `views_bp`) parse requests, call stores,
  catch domain errors and render templates. No business logic lives here.
- **Stores** (`src/volunteer.py`, `src/production.py`, `src/performance.py`,
  `src/crew_call.py`, `src/assignment.py`) hold the domain logic. Each store
  keeps its records in a dict keyed by id and raises the shared exceptions from
  `src/errors.py`.
- **Persistence** (`src/database.py`) saves a snapshot of all stores to SQLite
  and loads it back at startup; `src/storage.py` loads the CSV sample data.

## Application factory

`src/app.py` exposes `create_app()`, which:

1. Resolves the template directory (`templates/` at project root).
2. Bootstraps data at startup: if `DATABASE_URL` points to an existing file it
   is loaded; otherwise the CSV seed data is loaded when `SEED_DATA=true`
   (default), so a fresh checkout always starts with a working sample season.
3. Registers the `views` blueprint and error handlers.

Run it with:

```bash
python -m flask --app src.app run
```

## Routes

| Route | View | Purpose |
|---|---|---|
| `/` | `index` | Home page with quick links |
| `/productions` | `productions` | List productions with performance/role counts |
| `/productions/<id>` | `production_detail` | One production with its performances, crew calls and assignments |
| `/volunteers` | `volunteers` | List and create volunteers |
| `/personal/<volunteer_id>` | `personal_view` | A volunteer's personal roster |
| `/roster/<performance_id>` | `roster_gap_view` | Roster gap view for one performance |

## Error handling

`src/errors.py` defines three shared exception types so every store raises the
same errors:

- `ValidationError` — bad input (blank names, invalid email, ...)
- `NotFoundError` — record does not exist
- `RuleViolationError` — a domain rule (the one-role rule) would be broken

The views catch these and map them to HTTP 400 / 404 / 409 responses with
human-readable messages, so the web UI never shows a traceback.

## Key design decisions

| Decision | Why |
|---|---|
| SQLite, not PostgreSQL | RFP asks for a lightweight file-based store; zero configuration, survives restarts. See the decision comment on TR-TECH-03 in Jira. |
| Flask, not Django | Eight routes and forms do not justify Django's weight; Flask keeps the learning curve flat for the next maintainer. |
| One store module per entity | Each entity's rules live in one place (`*Store.create`), so the one-role rule has a single point of enforcement. |
| Business rules in stores, not views | Rules stay testable without a web server; 102 tests cover them directly. |
| Plain dicts + dataclasses, no ORM | Five entities do not justify SQLAlchemy; persistence is an explicit snapshot layer. |
