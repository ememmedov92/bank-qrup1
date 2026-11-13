from decimal import Decimal, InvalidOperation
from datetime import date

DAILY_DEPOSIT_LIMIT = Decimal("2000.00")
FREE_WITHDRAW_LIMIT = Decimal("500.00")
MAX_DAILY_WITHDRAWAL = Decimal("1000.00")
WITHDRAW_FEE_RATE = Decimal("0.02")


def to_decimal(value):
    return Decimal(str(value))


def to_storage(value):
    return float(value)


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
    if user.get("deposit_date") != today:
        user["deposit_total"] = 0.0
        user["deposit_date"] = today
    if user.get("withdraw_date") != today:
        user["withdraw_total"] = 0.0
        user["withdraw_date"] = today


def show_account_info(username, user):
    status = "Blocked" if user.get("is_blocked", False) else "Active"
    print(f"Account Holder: {username}")
    print(f"Account Number: {user['account_number']}")
    print(f"Current Balance: {to_decimal(user['balance']):.2f} AZN")
    print(f"Account Status: {status}")


def show_balance(user):
    print(f"Current Balance: {to_decimal(user['balance']):.2f} AZN")


def remaining_deposit_limit(user):
    reset_daily_if_new_day(user)
    return DAILY_DEPOSIT_LIMIT - to_decimal(user["deposit_total"])


def apply_deposit(user, amount, atm_cash):
    user["balance"] = to_storage(to_decimal(user["balance"]) + amount)
    user["deposit_total"] = to_storage(to_decimal(user["deposit_total"]) + amount)
    return to_decimal(atm_cash) + amount


def deposit(user, atm_cash):
    atm_cash = to_decimal(atm_cash)
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
    print(f"Deposit successful. New balance: {to_decimal(user['balance']):.2f} AZN")
    print(f"Remaining deposit limit: {remaining_deposit_limit(user):.2f} AZN")
    return atm_cash


def calculate_withdraw_fee(withdrawn_today, amount):
    free_left = max(Decimal("0.00"), FREE_WITHDRAW_LIMIT - withdrawn_today)
    fee_part = max(Decimal("0.00"), amount - free_left)
    return (fee_part * WITHDRAW_FEE_RATE).quantize(Decimal("0.01"))


def remaining_withdraw_limit(user):
    reset_daily_if_new_day(user)
    return MAX_DAILY_WITHDRAWAL - to_decimal(user["withdraw_total"])


def apply_withdrawal(user, amount, fee, atm_cash):
    user["balance"] = to_storage(to_decimal(user["balance"]) - amount - fee)
    user["withdraw_total"] = to_storage(to_decimal(user["withdraw_total"]) + amount)
    return to_decimal(atm_cash) - amount


def withdraw(user, atm_cash):
    atm_cash = to_decimal(atm_cash)
    text = input("Enter the amount to withdraw: ")
    amount = parse_amount(text)
    if amount is None:
        print("Error: the amount must be positive with at most 2 decimal places.")
        return atm_cash

    remaining = remaining_withdraw_limit(user)
    if amount > remaining:
        print(f"Withdrawal rejected: daily limit exceeded. Remaining limit: {remaining:.2f} AZN")
        return atm_cash

    fee = calculate_withdraw_fee(to_decimal(user["withdraw_total"]), amount)
    if to_decimal(user["balance"]) < amount + fee:
        print("Withdrawal rejected: insufficient balance (fee included).")
        return atm_cash

    if atm_cash < amount:
        print("Withdrawal rejected: not enough cash in the ATM.")
        return atm_cash

    atm_cash = apply_withdrawal(user, amount, fee, atm_cash)
    print(f"Withdrawal successful. Cash dispensed: {amount:.2f} AZN, fee: {fee:.2f} AZN")
    print(f"New balance: {to_decimal(user['balance']):.2f} AZN")
    return atm_cash


def show_daily_limits(user, outgoing_transfers=0):
    reset_daily_if_new_day(user)
    deposited = to_decimal(user["deposit_total"])
    withdrawn = to_decimal(user["withdraw_total"])
    free_left = max(Decimal("0.00"), FREE_WITHDRAW_LIMIT - withdrawn)

    print("DAILY LIMITS")
    print(f"Deposited today: {deposited:.2f}/{DAILY_DEPOSIT_LIMIT:.2f} AZN")
    print(f"Remaining deposit: {DAILY_DEPOSIT_LIMIT - deposited:.2f} AZN")
    print(f"Withdrawn cash: {withdrawn:.2f}/{MAX_DAILY_WITHDRAWAL:.2f} AZN")
    print(f"Remaining withdrawal: {MAX_DAILY_WITHDRAWAL - withdrawn:.2f} AZN")
    print(f"Remaining fee-free cash: {free_left:.2f} AZN")
    print(f"Outgoing transfers: {outgoing_transfers}/5")

