# Technology Selection

Owner: Li Qize (Technical Lead)
Related document: Section 4.1 of the Procurement Plan.

## Selected stack

| Component | Choice | Version | Licence | Rationale |
|---|---|---|---|---|
| Language | Python | 3.10+ (developed on 3.12) | PSF | RFP requirement; the team's core language |
| Web framework | Flask | 3.x | BSD-3-Clause | Lightweight; simple routing and forms for a small app |
| Database | SQLite via `sqlite3` | bundled | Public domain | Zero-configuration, file-based, survives restarts |
| Testing | pytest | 8+ | MIT | Concise assertions, fixtures, parametrisation |
| CI | GitHub Actions | — | Free tier | Runs the test suite on every push and PR |
| Container | Docker | Engine + Compose | Apache-2.0 | Reproducible demo and handover environment |

## Alternatives considered

| Component | Alternative | Why it was rejected |
|---|---|---|
| Web framework | Django | Batteries included, but too heavy for this scope; its ORM would fight the file-based requirement |
| Web framework | FastAPI | Great for APIs, but the app is a small CLI/web hybrid; Flask is simpler to teach to the next maintainer |
| Database | PostgreSQL | Requires a server; the RFP asks for a lightweight file-based store for local use |
| Database | JSON file | No query support and manual locking; SQLite gives the same single-file property with SQL |
| Testing | unittest | More verbose; pytest's fixtures reduce duplication across the 88 tests |
| CI | Jenkins | Requires hosting; GitHub Actions is free and already integrated with the repository |

## Feasibility summary

- All components are open source with zero licensing cost (see Procurement Plan 4.3).
- Every component installs with a single `pip install -r requirements.txt` command.
- The full test suite (88 tests) runs in under 5 minutes, satisfying the RFP non-functional requirement.
