import json
import os
import time
from datetime import datetime

FILE = "bank_data_v1.json"

today = datetime.now().strftime("%Y-%m-%d")


def new_user(account_number, password, balance):
    return {
        "account_number": account_number,
        "password": password,
        "balance": balance,
        "is_blocked": False,
        "failed_attempts": 0,
        "lockout_until": None,
        "deposit_date": today,
        "deposit_total": 0.0,
        "withdraw_date": today,
        "withdraw_total": 0.0,
        "transfer_date": today,
        "daily_transfer_count": 0,
        "last_login": None,
        "last_transaction_time": None,
        "history": [],
    }


default_data = {
    "atm_cash": 5000.0,
    "last_transaction_number": 0,
    "users": {
        "user01": new_user("10010001", "Test@123", 2500.0),
        "user02": new_user("10010002", "Test@456", 1500.0),
        "user03": new_user("10010003", "Test@789", 3000.0),
    },
}


def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "users" in data and "atm_cash" in data and "last_transaction_number" in data:
                return data
            print("Data file is invalid. Default data will be created.")
        except (json.JSONDecodeError, OSError):
            print("Data file is unreadable. Default data will be created.")
    save_data(default_data)
    return default_data


def countdown(seconds):
    while seconds > 0:
        seconds -= 1
        print(f"Please wait: 00:{seconds:02d}")
        time.sleep(1)


def login(data):
    name = input("Input name: ").strip()

    if name not in data["users"]:
        print("Invalid username.")
        return None

    user = data["users"][name]

    if user["is_blocked"]:
        print("Access denied. Your account is blocked.")
        return None

    if user["lockout_until"] is not None and user["lockout_until"] > time.time():
        remaining = int(user["lockout_until"] - time.time()) + 1
        print("Too many failed login attempts.")
        countdown(remaining)
        print("You may try again.")

    while user["failed_attempts"] < 6:
        password = input("Input your password: ")

        if password == user["password"]:
            print("Correct password")
            user["failed_attempts"] = 0
            user["lockout_until"] = None
            if user["last_login"]:
                print("Last login:", user["last_login"])
            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(data)
            print("Successfully logged in")
            return name

        user["failed_attempts"] += 1
        print(f"Incorrect password. Attempt: {user['failed_attempts']}/6\n")

        if user["failed_attempts"] == 3:
            print("Too many failed login attempts.")
            user["lockout_until"] = time.time() + 60
            save_data(data)
            countdown(60)
            print("You may try again.")

        elif user["failed_attempts"] == 6:
            print("Maximum login attempts exceeded.")
            print("Your card has been blocked.")
            print("Please contact the bank administrator.")
            user["is_blocked"] = True

        save_data(data)

    print("Access denied. Your account is blocked.")
    return None


def password_ok(new_password):
    if len(new_password) < 8:
        return False
    has_upper = False
    has_lower = False
    has_digit = False
    for ch in new_password:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
    return has_upper and has_lower and has_digit


def change_password(data, name):
    user = data["users"][name]

    old = input("Enter current password: ")
    if old != user["password"]:
        print("Wrong current password.")
        return

    new = input("Enter new password: ")
    if not password_ok(new):
        print("Password must have at least 8 characters, one uppercase letter, "
              "one lowercase letter and one digit.")
        return
    if new == user["password"]:
        print("New password must be different from the old password.")
        return

    again = input("Enter new password again: ")
    if new != again:
        print("Passwords do not match.")
        return

    user["password"] = new
    save_data(data)
    print("Password changed successfully.")


def main():
    data = load_data()
    name = login(data)
    if name is None:
        return

    while True:
        print("\n1. Change Password\n9. Logout\n0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            change_password(data, name)
        elif choice == "9" or choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


main()
