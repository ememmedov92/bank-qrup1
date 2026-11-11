import history

MAX_TRANSFERS_PER_DAY = 5


def find_username_by_account(data, account_number):
    for username in data["users"]:
        user = data["users"][username]
        if user["account_number"] == account_number:
            return username
    return None


def reset_transfer_counter_if_new_day(user):
    today = history.today_string()
    if user["transfer_date"] != today:
        user["transfer_date"] = today
        user["transfer_count"] = 0


def ask_yes_no(question):
    while True:
        answer = input(question).strip().upper()
        if answer == "Y":
            return True
        if answer == "N":
            return False
        print("Zehmet olmasa yalniz Y ve ya N daxil edin.")


def transfer_money(data, sender_username):
    sender = data["users"][sender_username]

    reset_transfer_counter_if_new_day(sender)
    if sender["transfer_count"] >= MAX_TRANSFERS_PER_DAY:
        print("Kocurme alinmadi: Bu gun artiq", MAX_TRANSFERS_PER_DAY, "defe kocurme etmisiniz.")
        return

    receiver_account = input("Alan sexsin hesab nomresi: ").strip()
    receiver_username = find_username_by_account(data, receiver_account)
    
    if receiver_username is None:
        print("Xeta: Bele hesab nomresi yoxdur.")
        return
    if receiver_username == sender_username:
        print("Xeta: Oz hesabiniza pul kocure bilmezsiniz.")
        return

    amount, error = history.read_amount(input("Mebleg (AZN): "))
    if error is not None:
        print("Xeta:", error)
        return

    receiver = data["users"][receiver_username]
    sender_balance = sender["balance"]
    receiver_balance = receiver["balance"]

    if amount > sender_balance:
        print("Xeta: Balansda kifayet qeder pul yoxdur. Sizin balansiniz:", history.money(sender_balance), "AZN.")
        return

    print("Gonderen:", sender_username)
    print("Alan hesab:", receiver_account)
    print("Mebleg:", history.money(amount), "AZN")
    
    if not ask_yes_no("Kocurmeni tesdiqleyirsiniz? (Y/N): "):
        print("Kocurme legv edildi.")
        return

    old_count = sender["transfer_count"]
    old_number = data["last_transaction_number"]

    sender["balance"] = sender_balance - amount
    receiver["balance"] = receiver_balance + amount
    sender["transfer_count"] = old_count + 1

    history.add_history_record(data, sender_username, "Kocurme Gonderildi", -amount,
                                sender_balance, sender["balance"], 0, receiver["account_number"])
    history.add_history_record(data, receiver_username, "Kocurme Alindi", amount,
                                receiver_balance, receiver["balance"], 0, sender["account_number"])

    if not history.save_data(data):
        sender["balance"] = sender_balance
        receiver["balance"] = receiver_balance
        sender["transfer_count"] = old_count
        sender["history"].pop()
        receiver["history"].pop()
        data["last_transaction_number"] = old_number
        print("Xeta: Melumat yadda saxlanilmadi, kocurme legv olundu.")
        return

    print("Kocurme uqurla tamamlandi!")
    print("Yeni balansiniz:", history.money(sender["balance"]), "AZN")


if __name__ == "__main__":
    all_data = history.load_data()
    transfer_money(all_data, "user01")
    history.show_history(all_data, "user01")