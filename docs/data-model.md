# Data Model

Owner: Li Qize (Technical Lead)
Implementation: `src/volunteer.py`, `src/production.py`, `src/performance.py`, `src/crew_call.py`, `src/assignment.py`

## Entity overview

```
Production 1 --- * Performance 1 --- * CrewCall (role, number needed)
                        |
                        * --- * Assignment * --- 1 Volunteer
                        |          |
                        |          role, status ("unconfirmed" | "confirmed")
```

- A **Production** (e.g. "The Weather House") has many **Performances**.
- Each **Performance** has one **CrewCall**: the set of roles and how many volunteers each role needs.
- An **Assignment** links one **Volunteer** to one role at one **Performance**.

## Entities

### Volunteer

| Field | Type | Notes |
|---|---|---|
| id | int | Auto-increment, assigned by the store |
| name | str | Required; blank names rejected; whitespace trimmed |
| phone | str | Optional |
| email | str | Optional |
| active | bool | Defaults to `True`; deactivation keeps history |
| created_at | datetime (UTC) | Set on creation |

Rules:
- `create` rejects blank names (`ValidationError`).
- `update` leaves fields unchanged when the argument is `None`.
- `deactivate` marks the volunteer inactive; existing records and assignments are preserved. Inactive volunteers cannot receive new assignments.

### Production

| Field | Type | Notes |
|---|---|---|
| id | int | Auto-increment |
| title | str | Required; blank titles rejected |

### Performance

| Field | Type | Notes |
|---|---|---|
| id | int | Auto-increment |
| production_id | int | Must reference an existing production (`NotFoundError` otherwise) |
| performance_date | date | ISO string `YYYY-MM-DD` or `date` object; malformed dates rejected |
| start_time | str | 24-hour `HH:MM`; validated by regex |

### CrewCall

Stored per performance as `{role: number_needed}`.

| Field | Type | Notes |
|---|---|---|
| performance_id | int | Must reference an existing performance |
| role | str | Required; non-blank |
| needed | int | Must be a positive whole number (`>= 1`) |

Rules:
- `set_requirement` creates or updates a role's count.
- `remove_role` removes a role (no-op if absent).
- `requirements_for` returns a defensive copy; callers cannot corrupt the store.

### Assignment

| Field | Type | Notes |
|---|---|---|
| id | int | Auto-increment |
| performance_id | int | Must reference an existing performance |
| volunteer_id | int | Must reference an existing, **active** volunteer |
| role | str | Required; non-blank |
| status | str | `"unconfirmed"` (default) or `"confirmed"` |

## The one-role rule (formal definition)

> A volunteer may hold **at most one role** in the same performance.

Enforcement:
- `AssignmentStore.create` raises `RuleViolationError` when the volunteer already holds an assignment for the same performance; the rejected assignment is not stored.
- `change` cannot break the rule: a volunteer can only ever hold one assignment in a performance, so changing its role or status is always safe.
- `remove` frees the volunteer for that performance; a new assignment for the same volunteer/performance pair is then allowed.

## Status model

```
unconfirmed ---- change(status="confirmed") ----> confirmed
    ^                                                  |
    |---- change(status="unconfirmed") ----------------|
```

Invalid status values are rejected (`ValidationError`); the only accepted values are `unconfirmed` and `confirmed`.

## Persistence (SQLite)

`src/storage.py` snapshots all five entities into a single SQLite database (`save_snapshot` / `load_snapshot`):

| Table | Key columns |
|---|---|
| volunteers | id, name, phone, email, active, created_at |
| productions | id, title |
| performances | id, production_id, performance_date, start_time |
| crew_calls | (performance_id, role) PRIMARY KEY, needed |
| assignments | id, performance_id, volunteer_id, role, status |

- `restore()` on each store rebuilds contents and the next-id counter, so new records never collide with restored ids.
- Sample data (`data/sample_volunteers.csv`, `data/sample_productions.csv`) is loaded with `load_seed_data`.
