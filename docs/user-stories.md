# User Stories and Acceptance Criteria

## Epic 1: Volunteers

### US-1: Create a volunteer record
As the volunteer coordinator, I want to add a volunteer to the company's list so that they can be rostered on a show.

**Acceptance Criteria:**
- I can record at minimum the volunteer's name and a way to contact them.
- A volunteer saved in one session is still there when the application is started again.
- I can make a volunteer inactive without destroying the assignments they have already worked.

### US-2: Find and update a volunteer
As the volunteer coordinator, I want to find and update a volunteer's details so that the list stays accurate.

**Acceptance Criteria:**
- I can search for a volunteer by name and get every match.
- I can change a volunteer's name, phone, or email.

### US-3: Deactivate a volunteer
As the volunteer coordinator, I want to deactivate a volunteer who has left so that they no longer appear as options when rostering.

**Acceptance Criteria:**
- A deactivated volunteer does not appear as an option when booking a new assignment.
- Their existing assignments are preserved.

## Epic 2: Productions and Performances

### US-4: Create a production
As the producer, I want to create a production and record its performances so that the season is visible in one place.

**Acceptance Criteria:**
- I can create a production with a title.
- I can add performances to it, each with a date and a start time.
- I can list the performances of a production in date and time order.

### US-5: Change or remove a performance
As the producer, I want to change or remove a performance so that the season reflects reality.

**Acceptance Criteria:**
- I can change or remove a performance.
- Other performances of the production are unaffected.

## Epic 3: Crew Calls

### US-6: Define a crew call for a performance
As the volunteer coordinator, I want to record the roles needed for a performance and how many people are needed in each.

**Acceptance Criteria:**
- I can record roles and the number needed for each.
- Different performances may have different calls.

## Epic 4: Assignments

### US-7: Assign a volunteer to a role
As the volunteer coordinator, I want to assign a volunteer to a role for a performance so that everyone knows who is on.

**Acceptance Criteria:**
- The assignment records the performance, the role and the volunteer.
- A saved assignment appears on that performance's roster.
- A new assignment starts as unconfirmed.

### US-8: One-role rule
As the volunteer coordinator, I want the system to refuse a second role for the same volunteer in the same performance, with a reason.

**Acceptance Criteria:**
- A volunteer may hold at most one role in any single performance.
- A duplicate assignment is refused with a reason.
- The same check applies when moving an existing assignment.

### US-9: Change or remove an assignment
As the volunteer coordinator, I want to change or remove an assignment so that the roster reflects who is actually coming.

**Acceptance Criteria:**
- I can replace the volunteer on an assignment, or remove it.
- Removing an assignment leaves that position open on the roster.
- Changing one assignment does not affect any other assignment.

## Epic 5: Views

### US-10: Roster gap view
As the volunteer coordinator, I want to see the roster for a performance or production, showing filled and open positions.

**Acceptance Criteria:**
- I can see which positions in the call are filled and which are still open.
- A performance with no assignments shows all positions open.

### US-11: Personal roster view
As a volunteer, I want to see the performances I am rostered on.

**Acceptance Criteria:**
- I can list my own assignments with the production, date, start time and role.
- I see only my own assignments, not the whole company's.
- A volunteer with no assignments gets an empty list rather than an error.
