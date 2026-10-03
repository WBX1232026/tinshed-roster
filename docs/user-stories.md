# User Stories and Acceptance Criteria

> Source of truth: team case study (Tinshed Players Inc.). Stories are split into the committed sprint backlog and a prioritised product backlog. Sprint scope is sized to what a small team can actually finish; everything Judith, Bec or Ravi asked for but that is deferred is recorded in the product backlog below with a reason.

## Sprint backlog (committed)

### Epic 1: Volunteers

#### US-1: Create a volunteer record
As the volunteer coordinator, I want to add a volunteer to the company's list so that they can be rostered on a show.

**Acceptance Criteria:**
- I can record at minimum the volunteer's name and a way to contact them (phone or email).
- A volunteer saved in one session is still there when the application is started again.
- I can make a volunteer inactive without destroying the assignments they have already worked.

#### US-2: Find and update a volunteer
As the volunteer coordinator, I want to find and update a volunteer's details so that the list stays accurate.

**Acceptance Criteria:**
- I can search for a volunteer by name and get every match.
- I can change a volunteer's name, phone, or email.

#### US-3: Deactivate a volunteer
As the volunteer coordinator, I want to deactivate a volunteer who has left so that they no longer appear as options when rostering.

**Acceptance Criteria:**
- A deactivated volunteer does not appear as an option when booking a new assignment.
- Their existing assignments are preserved.

### Epic 2: Productions and Performances

#### US-4: Create a production and its performances
As the producer, I want to create a production and record its performances so that the season is visible in one place.

**Acceptance Criteria:**
- I can create a production with a title.
- I can add performances to it, each with a date and a start time.
- I can list the performances of a production in date and time order.

#### US-5: Change or remove a performance
As the producer, I want to change or remove a performance so that the season reflects reality.

**Acceptance Criteria:**
- I can change or remove a performance.
- Other performances of the production are unaffected.

#### US-6: Define a crew call for a performance
As the volunteer coordinator, I want to record the roles needed for a performance and how many people are needed in each, so that I know what a show must be staffed with.

**Acceptance Criteria:**
- I can record roles and the number needed for each.
- Different performances may have different calls — an evening show and a matinee of the same production do not need the same call.
- A call records its call times: crew 60 minutes before curtain, front-of-house and box office 45 minutes before curtain.

### Epic 3: Assignments

#### US-7: Assign a volunteer to a role
As the volunteer coordinator, I want to assign a volunteer to a role for a performance so that everyone knows who is on.

**Acceptance Criteria:**
- The assignment records the performance, the role and the volunteer.
- A saved assignment appears on that performance's roster.
- A new assignment starts as unconfirmed.

#### US-8: One-role rule
As the volunteer coordinator, I want the system to refuse a second role for the same volunteer in the same performance, with a reason, so that no one is ever booked in two places at once.

**Acceptance Criteria:**
- A volunteer may hold at most one role in any single performance.
- A duplicate assignment is refused with a reason.
- The same check applies when moving an existing assignment to a different performance.

#### US-9: Change or remove an assignment
As the volunteer coordinator, I want to change or remove an assignment so that the roster reflects who is actually coming.

**Acceptance Criteria:**
- I can replace the volunteer on an assignment, or remove it.
- Removing an assignment leaves that position open on the roster.
- Changing one assignment does not affect any other assignment.

#### US-10: Track confirmed and notified separately
As the volunteer coordinator, I want to record whether an assignment is confirmed and whether the volunteer has been notified as two separate things, because they are not the same.

**Acceptance Criteria:**
- An assignment can be marked "confirmed" independently of whether the volunteer has been told.
- I can see at a glance who has not yet been notified.
- "Notified" and "confirmed" default to false for a new assignment.

### Epic 4: Views

#### US-11: Roster gap view
As the volunteer coordinator, I want to see the roster for a performance or production, showing filled and open positions.

**Acceptance Criteria:**
- I can see which positions in the call are filled and which are still open.
- A performance with no assignments shows all positions open.

#### US-12: Personal roster view
As a volunteer, I want to see the performances I am rostered on, so that I know when to arrive and what I am doing.

**Acceptance Criteria:**
- I can list my own assignments with the production, date, start time and role.
- I see only my own assignments, not the whole company's.
- A volunteer with no assignments gets an empty list rather than an error.

---

## Product backlog (deferred, prioritised)

| # | Story (summary) | Why it is deferred |
|---|---|---|
| PBI-1 | Track which volunteers are trained/qualified for each role (lights, sound, etc.) so the roster shows who can actually work a desk. | Ravi's top concern; "qualification matching" is explicitly out of scope for this sprint. Highest priority next. |
| PBI-2 | Record a volunteer's unavailable dates (e.g. "away 11–13 Sep for a wedding") and warn when rostering on those dates. | From the volunteer form (Kelly, TP-0142); directly prevents double-booking failures, but not in the core scope. |
| PBI-3 | Record RSA certificate and Blue Card details and flag when a bar role or 18+ cast requires them. | Out of scope ("checking RSA / Blue Card"); needs the legal data model done carefully. |
| PBI-4 | Enforce the "at least two ushers per performance" fire-regulation rule. | A hard business rule from the paper documents, but more than the core CRUD; add as validation later. |
| PBI-5 | Let volunteers swap shifts without going through the coordinator. | Bec's wish; adds self-service and notification complexity. |
| PBI-6 | Send a reminder (SMS/email) the day before a call. | Out of scope ("sending email or SMS"). |
| PBI-7 | Equipment inventory (dimmer rack, sound desk, lanterns) for grant applications. | Ravi's wish; out of scope ("equipment inventory"). |
| PBI-8 | Record emergency contact, membership number and T-shirt size on a volunteer. | From the volunteer form; useful but not needed to roster this sprint. |
| PBI-9 | Membership fees and renewals. | Out of scope; owned by the committee, not the roster. |
| PBI-10 | Ticketing and box-office sales (TicketNest). | Out of scope. |
| PBI-11 | Volunteer hours reporting and grant acquittal. | Out of scope. |
| PBI-12 | Detect venue booking clashes with other hall users. | Out of scope; Judith owns the calendar. |
