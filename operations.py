from datetime import date

from decimal import Decimal, InvalidOperation

DAILY_DEPOSIT_LIMIT = Decimal("2000.00")

FREE_WITHDRAW_LIMIT = Decimal("500.00")
MAX_DAILY_WITHDRAWAL = Decimal("1000.00")
WITHDRAW_FEE_RATE = Decimal("0.02")


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


def calculate_withdraw_fee(withdrawn_today, amount):
    free_left = max(Decimal("0.00"), FREE_WITHDRAW_LIMIT - withdrawn_today)
    fee_part = max(Decimal("0.00"), amount - free_left)
    return (fee_part * WITHDRAW_FEE_RATE).quantize(Decimal("0.01"))

def remaining_withdraw_limit(user):
    reset_daily_if_new_day(user)
    return MAX_DAILY_WITHDRAWAL - Decimal(user["withdrawn_today"])


def apply_withdrawal(user, amount, fee, atm_cash):
    user["balance"] = str(Decimal(user["balance"]) - amount - fee)
    user["withdrawn_today"] = str(Decimal(user["withdrawn_today"]) + amount)
    return atm_cash - amount


def withdraw(user, atm_cash):
    text = input("Enter the amount to withdraw: ")
    amount = parse_amount(text)
    if amount is None:
        print("Error: the amount must be positive with at most 2 decimal places.")
        return atm_cash

    remaining = remaining_withdraw_limit(user)
    if amount > remaining:
        print(f"Withdrawal rejected: daily limit exceeded. Remaining limit: {remaining:.2f} AZN")
        return atm_cash

    fee = calculate_withdraw_fee(Decimal(user["withdrawn_today"]), amount)
    if Decimal(user["balance"]) < amount + fee:
        print("Withdrawal rejected: insufficient balance (fee included).")
        return atm_cash

    if atm_cash < amount:
        print("Withdrawal rejected: not enough cash in the ATM.")
        return atm_cash

    atm_cash = apply_withdrawal(user, amount, fee, atm_cash)
    print(f"Withdrawal successful. Cash dispensed: {amount:.2f} AZN, fee: {fee:.2f} AZN")
    print(f"New balance: {Decimal(user['balance']):.2f} AZN")
    return atm_cash

def show_daily_limits(user, outgoing_transfers=0):
    reset_daily_if_new_day(user)
    deposited = Decimal(user["deposited_today"])
    withdrawn = Decimal(user["withdrawn_today"])
    free_left = max(Decimal("0.00"), FREE_WITHDRAW_LIMIT - withdrawn)

    print("DAILY LIMITS")
    print(f"Deposited today: {deposited:.2f}/{DAILY_DEPOSIT_LIMIT:.2f} AZN")
    print(f"Remaining deposit: {DAILY_DEPOSIT_LIMIT - deposited:.2f} AZN")
    print(f"Withdrawn cash: {withdrawn:.2f}/{MAX_DAILY_WITHDRAWAL:.2f} AZN")
    print(f"Remaining withdrawal: {MAX_DAILY_WITHDRAWAL - withdrawn:.2f} AZN")
    print(f"Remaining fee-free cash: {free_left:.2f} AZN")
    print(f"Outgoing transfers: {outgoing_transfers}/5")

