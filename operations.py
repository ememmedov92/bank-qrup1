from datetime import date

from decimal import Decimal, InvalidOperation

DAILY_DEPOSIT_LIMIT = Decimal("2000.00")


def parse_amount(text):
    text = text.strip()
    try:
        amount = Decimal(text)
    except InvalidOperation:
        return None
    if not amount.is_finite():
        return None
    if amount <= 0:
        return None
    if amount != amount.quantize(Decimal("0.01")):
        return None
    return amount

def reset_daily_if_new_day(user):
    today = date.today().isoformat()
    if user.get("limits_date") != today:
        user["deposited_today"] = "0.00"
        user["withdrawn_today"] = "0.00"
        user["limits_date"] = today

def show_account_info(user):
    status = "Blocked" if user.get("blocked", False) else "Active"
    print(f"Account holder: {user['username']}")
    print(f"Account number: {user['account_number']}")
    print(f"Available balance: {Decimal(user['balance']):.2f} AZN")
    print(f"Account status: {status}")


def show_balance(user):
    print(f"Available balance: {Decimal(user['balance']):.2f} AZN")


def remaining_deposit_limit(user):
    reset_daily_if_new_day(user)
    used_today = Decimal(user["deposited_today"])
    return DAILY_DEPOSIT_LIMIT - used_today


def apply_deposit(user, amount, atm_cash):
    user["balance"] = str(Decimal(user["balance"]) + amount)
    user["deposited_today"] = str(Decimal(user["deposited_today"]) + amount)
    return atm_cash + amount


def deposit(user, atm_cash):
    text = input("Enter the amount to deposit: ")
    amount = parse_amount(text)
    if amount is None:
        print("Error: the amount must be positive with at most 2 decimal places.")
        return atm_cash

    remaining = remaining_deposit_limit(user)
    if amount > remaining:
        print(f"Deposit rejected: daily limit would be exceeded. Remaining limit: {remaining:.2f} AZN")
        return atm_cash

    atm_cash = apply_deposit(user, amount, atm_cash)
    print(f"Deposit successful. New balance: {Decimal(user['balance']):.2f} AZN")
    print(f"Remaining deposit limit: {remaining_deposit_limit(user):.2f} AZN")
    return atm_cash

