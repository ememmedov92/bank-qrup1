from datetime import datetime
from decimal import Decimal

from authentication import load_data, save_data, login, change_password
from operations import (
    show_account_info, show_balance, deposit, withdraw,
    show_daily_limits, to_decimal, reset_daily_if_new_day,
)

# ---- Member C's part -------------------------------------------------
# Replace the body of this function with a call to Member C's transfer
# function (see transfer.py). It must receive the whole data dict and the
# username, and must save the file itself.
try:
    from transfer import transfer_money as _transfer_money
except ImportError:
    _transfer_money = None


def do_transfer(data, username):
    if _transfer_money is None:
        print("Transfer is not connected yet (ask Member C for the function name).")
        return
    _transfer_money(data, username)
# ----------------------------------------------------------------------


def add_history(data, user, tx_type, amount, fee, balance_before, balance_after):
    """Write one entry in the same format as the other history records."""
    data["last_transaction_number"] = data.get("last_transaction_number", 0) + 1
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user["history"].append({
        "id": f"TXN{data['last_transaction_number']:04d}",
        "date_time": now,
        "type": tx_type,
        "amount": float(amount),
        "fee": float(fee),
        "balance_before": float(balance_before),
        "balance_after": float(balance_after),
    })
    user["last_transaction_time"] = now


def do_deposit(data, user):
    balance_before = to_decimal(user["balance"])
    atm_before = to_decimal(data["atm_cash"])
    atm_after = deposit(user, atm_before)
    balance_after = to_decimal(user["balance"])
    if balance_after != balance_before:          # deposit succeeded
        add_history(data, user, "Deposit", balance_after - balance_before, 0,
                    balance_before, balance_after)
    data["atm_cash"] = float(atm_after)
    save_data(data)


def do_withdraw(data, user):
    balance_before = to_decimal(user["balance"])
    atm_before = to_decimal(data["atm_cash"])
    atm_after = withdraw(user, atm_before)
    balance_after = to_decimal(user["balance"])
    if balance_after != balance_before:          # withdrawal succeeded
        cash = atm_before - atm_after
        fee = (balance_before - balance_after) - cash
        add_history(data, user, "Withdrawal", cash, fee, balance_before, balance_after)
    data["atm_cash"] = float(atm_after)
    save_data(data)


def show_history(user):
    history = user.get("history", [])
    if not history:
        print("No transactions yet.")
        return
    for tx in history[-10:]:
        print(f"ID: {tx['id']} | {tx['date_time']} | {tx['type']} | "
              f"Amount: {tx['amount']:.2f} AZN | Fee: {tx.get('fee', 0):.2f} | "
              f"Before: {tx['balance_before']:.2f} | After: {tx['balance_after']:.2f}"
              + (f" | Other account: {tx['other_account']}" if "other_account" in tx else ""))


def show_limits(data, user):
    reset_daily_if_new_day(user)
    save_data(data)
    show_daily_limits(user, user.get("daily_transfer_count", 0))


def show_menu(username):
    print("\nPYTHON BANKING SYSTEM")
    print(f"Welcome, {username}!")
    print("1. View account information")
    print("2. Check balance")
    print("3. Deposit money")
    print("4. Withdraw money")
    print("5. Transfer money")
    print("6. Transaction history")
    print("7. Daily limits")
    print("8. Change password")
    print("9. Logout")
    print("0. Exit")


def menu(data, username):
    """Returns True to log in again (logout), False to exit the program."""
    user = data["users"][username]
    while True:
        show_menu(username)
        choice = input("Select an option: ").strip()
        if choice == "1":
            show_account_info(username, user)
        elif choice == "2":
            show_balance(user)
        elif choice == "3":
            do_deposit(data, user)
        elif choice == "4":
            do_withdraw(data, user)
        elif choice == "5":
            do_transfer(data, username)
        elif choice == "6":
            show_history(user)
        elif choice == "7":
            show_limits(data, user)
        elif choice == "8":
            change_password(data, username)
        elif choice == "9":
            print("Logged out.")
            return True
        elif choice == "0":
            print("Goodbye!")
            return False
        else:
            print("Invalid choice. Please enter a number from the menu.")


def main():
    data = load_data()
    while True:
        username = login(data)
        if username is None:
            break
        if not menu(data, username):
            break


if __name__ == "__main__":
    main()