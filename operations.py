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