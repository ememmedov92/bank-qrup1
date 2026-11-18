Bakudevs — Python Banking & ATM System

Team **BakuDevs** — Group 577E — Fundamentals of Programming — Three-person team project

Project goal

A console-based, multi-user Python banking and ATM management system. It simulates authentication, balances, cash deposits, cash withdrawals, daily limits, fee calculation, account-to-account transfers, transaction history, password management and persistent file storage. Balances, limits, ATM cash, history and security states survive a restart. Invalid requests are rejected without applying partial changes.

Python version and how to run

- **Python version:** 3.14.7
- 

```bash
git clone https://github.com/ememmedov92/bank-qrup1.git
cd bank-qrup1
python main.py
```

On the first run, if no valid data file exists, default data is created automatically.

## 3. Default demonstration accounts

| Username | Default password | Opening balance |
|----------|------------------|-----------------|
| user01   | Test@123         | 2,500.00 AZN    |
| user02   | Test@456         | 1,500.00 AZN    |
| user03   | Test@789         | 3,000.00 AZN    |

Each account has a unique account number (e.g. `10010001`). These are demonstration credentials only; no real credentials are stored in this repository.

## 4. Features and exact limits

### Authentication (Member A)
- Login with username and password; invalid usernames are handled safely.
- Failed attempts are tracked separately for every account.
- After **3** wrong attempts: login disabled for **60 seconds** with a visible per-second countdown (`00:59`, `00:58`, ...). The lockout end time is saved, so restarting does not bypass it.
- After the wait, **3 additional attempts** are allowed.
- After **6** total failed attempts: the card/account is **blocked permanently**, even the correct password cannot log in, and the state persists after restart.
- A successful login resets the failed-attempt counter.
- Password change: verify current password, new password ≥ 8 characters with at least one uppercase letter, one lowercase letter and one digit, must differ from the old password, entered twice and compared. Passwords are stored hashed with a salt and never appear in history or logs.

### Deposits, withdrawals and ATM cash (Member B)
| Parameter | Value |
|-----------|-------|
| Max total deposits per user per day | 2,000.00 AZN |
| Deposit commission | 0% |
| Daily commission-free withdrawal allowance | 500.00 AZN |
| Absolute daily withdrawal maximum | 1,000.00 AZN |
| Fee on cash above the free allowance | 2% of the excess portion only |
| Initial shared ATM cash | 5,000.00 AZN |

- Amounts must be positive, numeric, with at most two decimal places.
- A deposit that would exceed the remaining daily allowance is rejected as a whole (never reduced).
- Successful deposit: increases user balance **and** ATM cash.
- Withdrawal: user balance must cover cash + fee; cash must fit within the remaining 1,000 AZN limit; ATM must hold enough cash. The daily total counts dispensed cash only (not fees). The account is debited cash + fee; the ATM is reduced only by the cash dispensed.
- Any rejected or cancelled operation leaves balance, ATM cash and daily counters unchanged.
- The ATM cash balance never becomes negative; after restart the latest stored value is used.
- Daily limits screen shows deposit used/remaining, cash withdrawn/remaining, fee-free remaining and outgoing transfers (x / 5).

### Transfers, history and storage (Member C)
- Transfer by the receiver's unique account number; receiver must exist and differ from the sender.
- Positive amount, sufficient sender funds, **explicit Y/N confirmation**; cancellation changes nothing.
- Maximum **5 successful outgoing transfers per sender per calendar day** (failed/cancelled and incoming transfers do not count).
- Both balances are updated as one logical operation; the ATM cash is not changed by transfers.
- Transaction history is separate for each user. Each record has: unique ID, date/time, type, amount, balance before, balance after, fee, and the other account number for transfers. Types: Deposit, Withdrawal, Withdrawal Commission, Transfer Sent, Transfer Received. The last 10 operations are shown; an empty history shows a message.
- Data is saved after every successful operation and loaded at startup; missing or malformed files are handled safely.

### Calendar-aware daily reset
Daily deposit, withdrawal and transfer counters are compared with the stored date and reset only when the local calendar date changes, never on program restart.

## 5. File format and project directory structure

All data is stored in **JSON** (main file: `bank_data_v1.json`). Monetary values are stored as fixed decimals / integer minor units to avoid floating-point errors.

```
bank-qrup1/
├── datalarjsonlar/
│   └── bank_data_v1.json    # accounts, ATM cash, history, daily counters
├── .gitignore
├── README.md
├── auth.py                  # login, blocking, countdown, password change (Member A)
├── authentication.py        # authentication helper (Member A) – describe its role
├── history.py               # transaction history (Member C)
├── main.py                  # entry point and main menu
├── operations.py            # deposit, withdrawal, fees, limits, ATM cash (Member B)
├── tests_operations.py      # tests for operations.py (Member B)
└── transfer.py              # transfers (Member C)
```

Stored data: username, password hash + salt, account number, balance, active/blocked state, failed attempts, lockout expiry, date-specific deposit/withdrawal totals, daily transfer count, transaction history, last login, last transaction time, shared ATM cash.

## 6. Team members and responsibilities

| Member | GitHub | Primary modules | Responsibilities |
|--------|--------|-----------------|------------------|
| **Member A — Tahirli Cavidan** | MrCeyvd | `auth.py`, `authentication.py` | Login, failed-attempt tracking, 60-second countdown, account blocking, password change |
| **Member B — (full name)** | @royatagizade07 | `operations.py`, `tests_operations.py` | Balances, deposit limit, withdrawals, commission, ATM reserve, daily limits screen |
| **Member C — Memmedov Eli** | emmemmedov92 | `transfer.py`, `history.py`, `datalarjsonlar/` | Transfers, 5-transfer daily limit, transaction history, persistence coordination |

**Shared:** Git conflicts, code review, integration, test design, README, bug fixes and live defence.

### How the work was integrated
- After login, `auth.py` provides the logged-in account number to all other modules.
- Deposits and withdrawals from `operations.py` are available only after login, and are written to the history (`history.py`) and saved to the same data file.
- `transfer.py` uses the logged-in account as sender and records both sides in the history.
- All modules read and write the same file, `bank_data_v1.json`, so changes are shared.

## 7. Branch and Pull Request workflow

```
supermain
 └── develop
      ├── feature/authentication
      ├── feature/deposits-and-limits
      ├── feature/withdrawals-and-atm
      ├── feature/transfers
      ├── feature/transaction-history
      ├── feature/file-storage
      └── bugfix/input-validation
```

- `supermain` — stable final version only (the repository's main branch).
- `develop` — integration branch.
- `feature/*` — one branch per module, created from `develop`.
- `bugfix/*` — fixes merged into `develop` after verification.
- Every substantial feature is merged into `develop` through a **Pull Request reviewed by at least one other member**. After integration tests pass, `develop` is merged into `supermain`.
- Each member has at least 6 meaningful commits, spread across at least 7 different days.

## 8. Test cases

| # | Scenario | Expected result | Status |
|---|----------|-----------------|--------|
| 1 | Correct credentials | Successful login | ☐ |
| 2 | Three wrong passwords | Visible, persistent 60-second wait | ☐ |
| 3 | Six total wrong passwords | Account blocked | ☐ |
| 4 | Correct password on blocked account | Login prohibited | ☐ |
| 5 | Deposit 200 AZN | User balance and ATM cash increase | ☐ |
| 6 | 1,800 deposited today; request 300 | Whole deposit rejected; 200 remains | ☐ |
| 7 | Restart after depositing 1,800 | Daily deposit usage stays 1,800 | ☐ |
| 8 | Withdrawal exceeds balance | No changes | ☐ |
| 9 | Withdraw 250 after 400 today | 2% fee on 150 only (3.00 AZN) | ☐ |
| 10 | Withdraw 100 after 950 today | Whole withdrawal rejected | ☐ |
| 11 | ATM has 200; request 500 | Rejected | ☐ |
| 12 | Transfer user01 → user02 | Both balances and histories updated | ☐ |
| 13 | Sixth outgoing transfer | Rejected | ☐ |
| 14 | Transfer to unknown account | Friendly error; no changes | ☐ |
| 15 | Transfer cancelled | No changes | ☐ |
| 16 | Change password | Only new password works | ☐ |
| 17 | Restart application | Balances, histories, limits, lockouts persist | ☐ |
| 18 | Next calendar day | Daily counters reset | ☐ |
| 19 | Login as a different user | Only that user's data visible | ☐ |
| 20 | Invalid amount / menu choice | No crash, no balance change | ☐ |
| 21 | Transfer while ATM is empty | Transfer still succeeds | ☐ |
| 22 | Feature merged into develop | Reviewed by another member | ☐ |

Known limitations
- Console-only interface; no GUI.
- Single-process use only (no concurrent access to the JSON file).
- Optional extensions not implemented: *(list or write "none")*.
