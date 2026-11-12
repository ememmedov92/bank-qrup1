import json
import os
import time
from datetime import datetime

# Faylın saxlanılacağı qovluq və fayl adı
DATA_DIR = "datalarjsonlar"
FILE = os.path.join(DATA_DIR, "transfers.json")

default_data = {
    "users": {
        "user01": {"balance": 250000, "password": "Test@123", "accnumb": "100010001",
                    "userstatus": "active", "attemptcount": 0, "lockout_until": 0, "last_login": ""},
        "user02": {"balance": 150000, "password": "Test@456", "accnumb": "100010010",
                    "userstatus": "active", "attemptcount": 0, "lockout_until": 0, "last_login": ""},
        "user03": {"balance": 300000, "password": "Test@789", "accnumb": "100010011",
                    "userstatus": "active", "attemptcount": 0, "lockout_until": 0, "last_login": ""},
    }
}


def save_data(data):
    # Əgər 'datalarjsonlar' qovluğu yoxdursa, avtomatik yaradır
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_data():
    """Fayl yoxdursa və ya xarabdırsa default data yaradır."""
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "users" in data:
                return data
            print("Data file is invalid. Default data will be created.")
        except (json.JSONDecodeError, OSError):
            print("Data file is unreadable. Default data will be created.")
    save_data(default_data)
    return default_data

def countdown(san):
    while san > 0:
        san -= 1
        print(f"Please wait: 00:{san:02d}")
        time.sleep(1)

def login(data):
    name = input("Input name: ").strip()

    if name not in data["users"]:
        print("Invalid username.")
        return None

    user = data["users"][name]

    if user["userstatus"] == "blocked":
        print("Access denied. Your account is blocked.")
        return None

    if user["lockout_until"] > time.time():
        qalan = int(user["lockout_until"] - time.time()) + 1
        print("Too many failed login attempts.")
        countdown(qalan)
        print("You may try again.")

    while user["attemptcount"] < 6:
        password = input("Input your password: ")

        if password == user["password"]:
            print("Correct password")
            user["attemptcount"] = 0
            user["lockout_until"] = 0
            if user["last_login"]:
                print("Last login:", user["last_login"])
            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(data)
            print("Successfully logged in")
            return name

        user["attemptcount"] += 1
        print(f"Incorrect password. Attempt: {user['attemptcount']}/6\n")

        if user["attemptcount"] == 3:
            print("Too many failed login attempts.")
            user["lockout_until"] = time.time() + 60
            save_data(data) 
            countdown(60)
            print("You may try again.")

        elif user["attemptcount"] == 6:
            print("Maximum login attempts exceeded.")
            print("Your card has been blocked.")
            print("Please contact the bank administrator.")
            user["userstatus"] = "blocked"

        save_data(data)

    print("Access denied. Your account is blocked.")
    return None


def password_ok(new_password):
    """Ən azı 8 simvol, 1 böyük hərf, 1 kiçik hərf, 1 rəqəm."""
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


if __name__ == "__main__":
    main()
