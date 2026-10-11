# Acceptance Criteria (Given / When / Then)

> Owner: Yao Tingran (Business/Requirements Lead). Each story below is written in Given/When/Then form, matching the Jira story issues (US-01 … US-12).

## Epic 1: Volunteers

### US-01 — Create a volunteer record
- **Given** the volunteer coordinator is on the volunteer list
- **When** they add a volunteer with a name and a phone number
- **Then** the volunteer appears in the list, the record survives an application restart, and it can later be deactivated without losing its past assignments.

### US-02 — Find and update a volunteer
- **Given** one or more volunteers already exist
- **When** the coordinator searches by name and edits a volunteer's name, phone or email
- **Then** every matching volunteer is returned, and the edited fields are saved while the others are unchanged.

### US-03 — Deactivate a volunteer
- **Given** a volunteer who has already worked some assignments
- **When** the coordinator deactivates that volunteer
- **Then** the volunteer no longer appears as an option when creating new assignments, and all existing assignments are preserved.

## Epic 2: Productions and Performances

### US-04 — Create a production and its performances
- **Given** the producer wants to record a new show
- **When** they create a production and add performances, each with a date and start time
- **Then** the production is created and its performances are listed in date and time order.

### US-05 — Change or remove a performance
- **Given** a production already has several performances
- **When** the producer changes or removes one performance
- **Then** that performance is updated or removed and the other performances are unaffected.

### US-06 — Define a crew call for a performance
- **Given** a performance needs to be staffed
- **When** the coordinator records the roles and the number needed for each, with call times (crew 60 min, FOH/box office 45 min before curtain)
- **Then** the call is recorded, and an evening show and a matinee of the same production may carry different calls.

## Epic 3: Assignments

### US-07 — Assign a volunteer to a role
- **Given** a volunteer, a performance and a role exist
- **When** the coordinator assigns the volunteer to that role for that performance
- **Then** the assignment is saved, it appears on the performance's roster, and it starts as "unconfirmed".

### US-08 — One-role rule
- **Given** a volunteer already holds a role on a performance
- **When** the coordinator tries to assign the same volunteer a second role on the same performance (or moves an assignment to do so)
- **Then** the system refuses with a reason and the duplicate assignment is not stored.

### US-09 — Change or remove an assignment
- **Given** an assignment exists on a performance
- **When** the coordinator replaces its volunteer or removes the assignment
- **Then** the assignment is updated or removed, the position is left open when removed, and no other assignment is affected.

### US-10 — Track confirmed and notified separately
- **Given** an assignment has been created (defaults to unconfirmed / not-notified)
- **When** the coordinator marks it confirmed, independently of notification
- **Then** confirmed and notified are stored as two separate flags, and the coordinator can see at a glance who has not yet been notified.

## Epic 4: Views

### US-11 — Roster gap view
- **Given** a performance has a crew call and some assignments
- **When** the coordinator opens the roster for that performance (or production)
- **Then** filled positions and still-open positions are shown, and a performance with no assignments shows every position open.

### US-12 — Personal roster view
- **Given** a volunteer has one or more assignments
- **When** they open their personal roster
- **Then** they see only their own assignments with production, date, start time and role (in chronological order), and a volunteer with no assignments gets an empty list rather than an error.
