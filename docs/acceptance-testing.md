# Acceptance Testing Record

## Test Scenarios

### Scenario 1: Create a volunteer
1. Start the application.
2. Create a volunteer with name "Col Hendricks", phone "0400 111 222".
3. Confirm the volunteer appears in the list.
4. Restart the application.
5. Confirm the volunteer is still there.
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
