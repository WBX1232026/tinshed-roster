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
