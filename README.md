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
### Member B — Core Transactions, Limits & ATM Cash Management (`@royatagizade07`)

This module is responsible for processing all financial transactions while enforcing account balances, transaction fees, daily withdrawal limits, and physical ATM cash constraints.

#### Key Features & Logic
* **Deposit Handling:**
  * Accepts valid positive deposit amounts (rejecting zero or negative inputs).
  * Immediately updates the user's account balance and adds the deposited cash to the ATM's total available cash reserve.
* **Withdrawal Processing & Fees:**
  * Validates that the requested amount is positive and meets minimum/multiple denomination rules.
  * Calculates applicable transaction fees (`fee`) and verifies that `withdrawal_amount + fee <= user_balance` before approving the transaction.
  * Deducts the total amount (withdrawal + fee) from the user's account and reduces the ATM's physical cash pool by the dispensed amount.
* **Daily Withdrawal Limits:**
  * Tracks each user's cumulative withdrawals within a 24-hour / daily cycle.
  * Blocks transactions if `daily_withdrawn + withdrawal_amount > daily_limit`, displaying the remaining daily allowance to the user.
* **ATM Cash Reserve Check:**
  * Verifies physical cash availability inside the ATM (`withdrawal_amount <= atm_cash`) prior to dispensing funds.
  * Prevents partial or failed dispenses by alerting the user if the ATM lacks sufficient cash, without altering their account balance.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------## Member C: Transfers, Transaction History and File Storage
**Author:** Memmedov Eli (emmemmedov92)
**Main modules:** `transfer.py`, `history.py`, `datalarjsonlar/`

### What this part does
Member C's module handles moving money between accounts, recording every operation, and saving all data to files. It works only after the user has logged in through `auth.py`.

### 1. Transfers
- The logged-in user enters the receiver's account number and the amount.
- The program checks that the receiver account exists and is not the same as the sender.
- The amount must be positive and not greater than the sender's balance.
- If all checks pass, the amount is subtracted from the sender and added to the receiver.
- If any check fails, an error message is shown and no balance is changed.

### 2. Transaction history
- Every operation (deposit, withdrawal, transfer sent, transfer received) is recorded with its type, amount, date and time.
- The user can view the history of their own account only.
- Transactions are shown in order, so the user can see what happened and when.

### 3. File storage
- All account data (balances, passwords, block status) and history are saved in JSON files in the `datalarjsonlar/` folder (main file: `bank_data_v1.json`).
- Data is saved after every successful operation, so nothing is lost when the program is closed.
- When the program starts, the data is loaded from the file again.

### Integration with other modules
- **Member A (authentication):** the account number of the logged-in user from `auth.py` is used as the sender of a transfer and to select whose history is shown.
- **Member B (ATM operations):** deposits and withdrawals made in `operations.py` are written to the history and saved to the same data file.
- All modules read and write the same data file (`bank_data_v1.json`), so changes are shared.

### What I can explain in the defense
- How a transfer is validated and how both balances are updated.
- How each operation is recorded in the history.
- How data is saved to and loaded from the JSON file.
- How my module is connected to login (Member A) and ATM operations (Member B).
