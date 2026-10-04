# Acceptance Testing Record

## Test Scenarios

### Scenario 1: Create a volunteer
1. Start the application.
2. Create a volunteer with name "Col Hendricks", phone "0400 111 222".
3. Confirm the volunteer appears in the list.
4. Restart the application.
5. Confirm the volunteer is still there.
**Result:** PASS

### Scenario 2: One-role rule
1. Create a volunteer.
2. Create a performance.
3. Assign the volunteer to "Bar 1" for that performance.
4. Try to assign the same volunteer to "Sound Op" for the same performance.
5. Confirm the second assignment is refused with a reason.
**Result:** PASS

### Scenario 3: Roster gap view
1. Create a performance with a crew call.
2. Assign one volunteer.
3. View the roster.
4. Confirm filled and open positions are shown correctly.
**Result:** PASS

### Scenario 4: Personal roster view
1. Create a volunteer.
2. Assign the volunteer to two performances.
3. View the volunteer's assignments.
4. Confirm both assignments are shown, and no other volunteer's assignments appear.
**Result:** PASS

## Summary

| Scenario | Result |
|---|---|
| Create a volunteer | PASS |
| One-role rule | PASS |
| Roster gap view | PASS |
| Personal roster view | PASS |
