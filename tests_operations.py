import builtins
import contextlib
import io
from datetime import date
from decimal import Decimal

from operations import (
    deposit, withdraw, calculate_withdraw_fee, remaining_deposit_limit,
    remaining_withdraw_limit,
)

TODAY = date.today().isoformat()
results = []


def new_user(balance=2500.0, dep=0.0, wd=0.0, day=None):
    day = day or TODAY
    return {
        "account_number": "10010001",
        "balance": balance,
        "deposit_date": day, "deposit_total": dep,
        "withdraw_date": day, "withdraw_total": wd,
    }


def run(func, user, atm, typed):
    """Run deposit/withdraw with a fake keyboard input; hide the printed text."""
    builtins_input = builtins.input
    builtins.input = lambda prompt="": typed
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return func(user, atm)
    finally:
        builtins.input = builtins_input


def check(name, condition):
    results.append(condition)
    print(("PASS  " if condition else "FAIL  ") + name)


# 5: deposit 200
u = new_user()
atm = run(deposit, u, 5000.0, "200")
check("5  Deposit 200: balance 2700, ATM 5200", u["balance"] == 2700.0 and atm == Decimal("5200.0"))

# 6: 1800 already deposited, try 300
u = new_user(dep=1800.0)
atm = run(deposit, u, 5000.0, "300")
check("6  Deposit 300 after 1800 is rejected, nothing changes",
      u["balance"] == 2500.0 and u["deposit_total"] == 1800.0 and atm == Decimal("5000.0"))
check("6  Remaining deposit limit is 200", remaining_deposit_limit(u) == Decimal("200"))

# deposit exactly up to the limit is allowed
u = new_user(dep=1800.0)
atm = run(deposit, u, 5000.0, "200")
check("6b Deposit exactly 200 after 1800 is accepted", u["deposit_total"] == 2000.0)

# 8: withdrawal larger than balance
u = new_user(balance=100.0)
atm = run(withdraw, u, 5000.0, "500")
check("8  Withdraw more than balance: nothing changes",
      u["balance"] == 100.0 and u["withdraw_total"] == 0.0 and atm == Decimal("5000.0"))

# 8b: balance covers the amount but not the fee
u = new_user(balance=300.0, wd=400.0)
atm = run(withdraw, u, 5000.0, "300")
check("8b Balance covers amount but not fee: rejected",
      u["balance"] == 300.0 and u["withdraw_total"] == 400.0)

# 9: 400 already withdrawn, request 250 -> fee 3.00
check("9  Fee for 250 after 400 is 3.00", calculate_withdraw_fee(Decimal("400"), Decimal("250")) == Decimal("3.00"))
u = new_user(balance=3000.0, wd=400.0)
atm = run(withdraw, u, 5000.0, "250")
check("9  Balance 2747, withdrawn today 650, ATM 4750",
      u["balance"] == 2747.0 and u["withdraw_total"] == 650.0 and atm == Decimal("4750.0"))

# 10: 950 already withdrawn, request 100
u = new_user(balance=3000.0, wd=950.0)
atm = run(withdraw, u, 5000.0, "100")
check("10 Withdraw 100 after 950 is rejected, nothing changes",
      u["balance"] == 3000.0 and u["withdraw_total"] == 950.0 and atm == Decimal("5000.0"))
check("10 Remaining withdraw limit is 50", remaining_withdraw_limit(u) == Decimal("50"))

# 11: ATM has only 200
u = new_user(balance=3000.0)
atm = run(withdraw, u, 200.0, "500")
check("11 ATM has 200, request 500: rejected",
      u["balance"] == 3000.0 and atm == Decimal("200.0"))

# 18: new calendar day resets counters
u = new_user(dep=1800.0, wd=400.0, day="2020-01-01")
check("18 New day: deposit limit is 2000 again", remaining_deposit_limit(u) == Decimal("2000"))
check("18 New day: counters reset to 0",
      u["deposit_total"] == 0.0 and u["withdraw_total"] == 0.0 and u["deposit_date"] == TODAY)

# 20: invalid input must never crash or change anything
for bad in ["abc", "-5", "0", "1.234", "", "   ", "NaN", "Infinity"]:
    for func in (deposit, withdraw):
        u = new_user()
        try:
            atm = run(func, u, 5000.0, bad)
            ok = u["balance"] == 2500.0 and atm == Decimal("5000.0")
        except Exception:
            ok = False
        check(f"20 {func.__name__} with {bad!r}: no crash, nothing changes", ok)

print()
print(f"{sum(results)}/{len(results)} checks passed")