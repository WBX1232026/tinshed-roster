# One-Role Rule

Owner: Li Qize (Technical Lead)
Jira: US-8 (story), TR-TECH-02 (design), TR-TECH-08 (implementation),
TR-BUG-02 (duplicate assignment bug, fixed)

## The rule

> A volunteer may hold **at most one role per performance**.

In other words: the same volunteer cannot be assigned twice to the same
performance, even for different roles. Different performances are independent —
a volunteer may hold many roles across a season.

## Why it exists

Without the rule, a volunteer could silently be double-booked for one show
(assigned both "Stage Manager" and "Lighting"), which would leave the roster
short-handed on the night. The rule comes from the business requirement (US-8)
and is enforced in one place only.

## Where it is enforced

Single point of enforcement: `AssignmentStore.create` in `src/assignment.py`.

```python
def create(self, volunteer_id, performance_id, role, ...):
    # ...validate volunteer/performance...
    for existing in self._assignments.values():
        if (existing.volunteer_id == volunteer_id
                and existing.performance_id == performance_id):
            raise RuleViolationError(
                "Volunteer already has a role in this performance."
            )
    # ...store the new assignment...
```

This is deliberate: every code path that creates an assignment (CLI, web view,
future imports) passes through `create`, so the rule can never be bypassed.

## How the UI reports it

`src/views.py` catches `RuleViolationError` and returns HTTP **409 Conflict**
with the message above, so the web form shows a clear error instead of a
duplicate row. The roster gap view counts roles from confirmed assignments, so
a second role for one volunteer would otherwise distort the gap calculation —
the rule prevents that data from ever existing.

## Tests

The rule was developed test-first (TDD): tests were written before the
enforcement code, per `docs/testing-strategy.md`.

| File | What it covers |
|---|---|
| `tests/test_one_role_rule.py` | Web-level: assigning the same volunteer twice returns 409; different performances are allowed |
| `tests/test_store_one_role_rule.py` | Store-level: `create` raises `RuleViolationError` for duplicates |
| `tests/test_assignment.py` | Assignment CRUD incl. moving an assignment (change role) within the rule |
| `tests/test_regression.py` | Regression: TR-BUG-02 scenario stays fixed |

Run the rule's suites alone:

```bash
pytest tests/test_one_role_rule.py tests/test_store_one_role_rule.py
```

## History

- **Design** (TR-TECH-02, Sprint 1): rule specified, decision recorded on the
  Jira issue.
- **Implementation** (TR-TECH-08, Sprint 2): enforced in `AssignmentStore.create`
  with tests first (PR #10).
- **Bug TR-BUG-02** (Sprint 2): before the fix, `create` allowed a second role
  for the same volunteer in one performance. Closed after PR #10; regression
  test added in PR #24.
