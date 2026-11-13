CAVIDAN a
ROYA b
MEMMEDOV ELI c
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Member A: Login, Blocking, Waiting Time and Password Change
**Author:** Tahirli Cavidan (MrCeyvd)
**Main module:** `auth.py`

### What this part does
Member A's module is the entry point of the system. A user can use deposit, withdrawal, transfers or history only after passing through this module.

### 1. Login
- The user enters the account number and password.
- The program checks them against the accounts stored in the JSON file.
- If both are correct, the user is logged in and gets access to the main menu.
- If the account number does not exist or the password is wrong, an error message is shown.

### 2. Account blocking
- Every wrong password attempt is counted.
- After 3 failed attempts, the account is temporarily blocked.
- A blocked account cannot log in, even with the correct password, until the block ends.
- The counter is reset after a successful login.

### 3. 60-second wait
- A blocked user must wait 60 seconds.
- The block time is saved with the account data, so restarting the program does not remove the block.
- After 60 seconds the account is unblocked automatically.
- While waiting, the program shows the remaining seconds.

### 4. Password change
- Only a logged-in user can change the password.
- The user enters the current password, then the new password (and confirms it).
- If the current password is wrong or the confirmation does not match, nothing is changed.
- The new password is saved to the JSON file.

### Integration with other modules
- **Member B (ATM operations):** deposit, withdrawal, fee and limits are available only after a successful login.
- **Member C (transfers, history, storage):** uses the logged-in account number from `auth.py` to identify the sender and whose history to show.
- All modules use the same data file (`bank_data_v1.json`).

### What I can explain in the defense
- How the login check works and where the data comes from.
- How failed attempts are counted and when an account is blocked.
- How the 60-second wait is calculated and saved.
- How the password change is validated.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
Read.me file
What is there now
In the README written so far:
• There is a place for all three names,  Roya Tagizade Tahirli Cavidan and Memmedov Eli are  royatagizade07 emmemmedov92 MrCeyvd
• Member B A and C's section is fully written (deposit, withdrawal, fee, limits).

What the specification requires

Who
What they write
Member B 
The "Member B section" withdrawals and deposits checking daily limits and ATM cash
 





All together
Shared sections: how to run, default accounts, Git flow, tests
Avoiding conflicts
If all three of you edit the same file at the same time, Git can produce a conflict. To prevent this:
1.  One person (for example the repo owner) puts the main version of the README into the repository.
2.  After that, everyone writes only their own section.
3.  Everyone makes a separate commit. This shows each of your contributions to the README.
4.  Do not touch each other's sections.
Message to your teammates
"We are writing the README together. I have prepared the Member B section. everyone write its own section
