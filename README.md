# 577E-Python-Banking-System

Console-based banking/ATM simulation in Python. Users log in, deposit, withdraw, transfer money and view history. All data is stored in JSON, so nothing is lost when the program closes.

## Run

Requires **Python 3.10+** (standard library only).

```bash
git clone https://github.com/<user>/577E-Python-Banking-System.git
cd 577E-Python-Banking-System
python main.py
```

Tests: `python -m unittest tests_operations -v`

## Demo Accounts

| User | Account number | Password | Balance (AZN) |
|------|----------------|----------|---------------|
| `user01` | `10010001` | `Test@123` | 2150.00     |
| `user02` | `10010002` | `Test@456` | 1850.00     |
| `user03` | `10010003` | `Test@789` | 3000.00     |

ATM starting cash: **5000.00 AZN**. Use `10010001` -> `10010002` for transfer demos; `user03` has an empty history.

## Features and Limits

- **Login:** account number + password. **3** wrong attempts block the account for **60 seconds** (saved in JSON, survives restart).
- **Password change:** current password + new password + confirmation.
- **Deposit:** amount must be > 0.
- **Withdrawal:** min `<10>` AZN, multiples of `<10>`, fee `<fee>`, daily limit `<limit>` AZN, must not exceed balance or ATM cash.
- **Transfer:** receiver must exist and differ from sender; amount > 0 and <= balance. On any error, nothing changes.
- **History:** deposit, withdrawal, transfer sent/received with type, amount, date and time. Users see only their own.
- **Storage:** data saved after every successful operation.

## Structure

```
main.py               entry point, menu
auth.py               login, blocking, password change   (A)
authentication.py     authentication helpers             (A)
operations.py         deposit, withdrawal, limits, ATM   (B)
tests_operations.py   unit tests                         (B)
transfer.py           transfers                          (C)
history.py            transaction history                (C)
datalarjsonlar/bank_data_v1.json   shared data file
```

JSON example (`bank_data_v1.json`):

```json
{
  "atm_cash": 5000.0,
  "last_transaction_number": 10,
  "users": {
    "user01": {
      "account_number": "10010001",
      "password": "Test@123",
      "balance": 2150.0,
      "is_blocked": false,
      "failed_attempts": 0,
      "lockout_until": null,
      "deposit_total": 0.0,
      "withdraw_total": 0.0,
      "transfer_count": 0,
      "history": [
        {
          "id": "TXN0001",
          "date_time": "2026-11-11 22:14:29",
          "type": "Kocurme Gonderildi",
          "amount": -50.0,
          "fee": 0,
          "balance_before": 2500.0,
          "balance_after": 2450.0,
          "other_account": "10010002"
        }
      ]
    }
  }
}
```

History types: `Kocurme Gonderildi` (transfer sent), `Kocurme Alindi` (transfer received), plus deposit and withdrawal records.

## Team

| Member | GitHub | Responsibility |
|--------|--------|----------------|
| A – Tahirli Cavidan | MrCeyvd | Login, blocking, 60 s wait, password change |
| B – Roya Tagizade | @royatagizade07 | Deposit, withdrawal, fee, limits, ATM cash |
| C – Memmedov Eli | emmemmedov92 | Transfers, history, JSON storage |

## Git Workflow

```
main
 └── develop
      ├── feature/authentication
      ├── feature/deposits-and-limits
      ├── feature/withdrawals-and-atm
      ├── feature/transfers
      ├── feature/transaction-history
      ├── feature/file-storage
      └── bugfix/input-validation
```

Each feature is built on its own branch from `develop`, merged via Pull Request with a teammate's review. `develop` goes into `main` when stable.

## Test Cases

| Scenario | Expected |
|----------|----------|
| Correct login | Menu opens |
| Wrong password x3 | Blocked 60 s, remaining seconds shown |
| Login while blocked | Refused, even with correct password |
| Deposit 0 or negative | Rejected |
| Withdraw > balance (with fee) | Rejected, balance unchanged |
| Withdraw over daily limit | Rejected, remaining allowance shown |
| Withdraw > ATM cash | Rejected, balance unchanged |
| Transfer to self / unknown account | Rejected |
| Transfer > balance | Rejected, no change |
| Restart program | Balances and history preserved |

## Known Limitations

- Passwords stored in plain text (no hashing).
- No protection against several instances writing the JSON file at once.
- Console only, single currency.
- Block time and daily limit depend on the system clock.
