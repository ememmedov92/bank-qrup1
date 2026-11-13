import json
import os
from datetime import datetime

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_FOLDER, "datalarjsonlar")
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")


def get_today_date():
    bugun = datetime.now()
    yil = str(bugun.year)
    ay = str(bugun.month)
    gun = str(bugun.day)
    
    if len(ay) == 1:
        ay = "0" + ay
    if len(gun) == 1:
        gun = "0" + gun
        
    return yil + "-" + ay + "-" + gun

def get_current_time():
    indiki_vaxt = datetime.now()
    return indiki_vaxt.strftime("%Y-%m-%d %H:%M:%S")


def format_money(mebleg):
    return f"{float(mebleg):.2f}"

def read_amount(metn):
    metn = metn.strip()
    
    if metn == "":
        return None, "Mebleg bosh ola bilmez."
    
    for simvol in metn:
        if not (simvol.isdigit() or simvol == "."):
            return None, "Zehmet olmasa yalniz reqem daxil edin."
            
    if metn.count(".") > 1:
        return None, "Duzgun format deyil. Meselen: 150.50"
        
    try:
        mebleg = float(metn)
    except:
        return None, "Yanlish mebleg daxil edildi."
        
    if mebleg <= 0:
        return None, "Mebleg 0-dan boyuk olmalidir."
        
    return mebleg, None


def load_json_file(yol):
    if not os.path.exists(yol):
        return None
    
    try:
        fayl = open(yol, "r", encoding="utf-8")
        verilenler = json.load(fayl)
        fayl.close()
        return verilenler
    except:
        return None

def save_json_file(yol, verilenler):
    try:
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)
            
        fayl = open(yol, "w", encoding="utf-8")
        json.dump(verilenler, fayl, indent=4)
        fayl.close()
        return True
    except:
        return False


def make_new_user(hesab_nomresi, sifre, balans):
    bugun = get_today_date()
    return {
        "account_number": hesab_nomresi,
        "password": sifre,
        "balance": balans,
        "is_blocked": False,
        "failed_attempts": 0,
        "lockout_until": None,
        "deposit_date": bugun,
        "deposit_total": 0.0,
        "withdraw_date": bugun,
        "withdraw_total": 0.0,
        "transfer_date": bugun,
        "transfer_count": 0,
        "last_login": None,
        "last_transaction_time": None,
        "history": []
    }

def create_default_data():
    return {
        "atm_cash": 5000.0,
        "last_transaction_number": 0,
        "users": {
            "user01": make_new_user("10010001", "Test@123", 2500.0),
            "user02": make_new_user("10010002", "Test@456", 1500.0),
            "user03": make_new_user("10010003", "Test@789", 3000.0)
        }
    }

def load_data():
    verilenler = load_json_file(USERS_FILE)
    
    if verilenler == None or "users" not in verilenler:
        verilenler = create_default_data()
        save_json_file(USERS_FILE, verilenler)
        
    return verilenler

def save_data(verilenler):
    return save_json_file(USERS_FILE, verilenler)


def add_history_record(data, username, record_type, amount, balance_before, balance_after, fee=0.0, other_account=None):
    user = data["users"][username]
    
    data["last_transaction_number"] = data["last_transaction_number"] + 1
    txn_no = data["last_transaction_number"]
    
    id_metni = str(txn_no)
    if len(id_metni) == 1:
        id_metni = "000" + id_metni
    elif len(id_metni) == 2:
        id_metni = "00" + id_metni
    elif len(id_metni) == 3:
        id_metni = "0" + id_metni
        
    transaction_id = "TXN" + id_metni
    
    vaxt = get_current_time()
    
    record = {
        "id": transaction_id,
        "date_time": vaxt,
        "type": record_type,
        "amount": amount,
        "fee": fee,
        "balance_before": balance_before,
        "balance_after": balance_after,
        "other_account": other_account
    }
    
    user["history"].append(record)
    user["last_transaction_time"] = vaxt
    
    return record

def show_history(data, username):
    history = data["users"][username]["history"]
    
    if len(history) == 0:
        print("Hele hech bir emeliyyatiniz yoxdur.")
        return
        
    print("\n======= TRANZAKSIYA TARIXCHESI =======")
    
    son_on = history[-10:]
    son_on.reverse()
    
    for record in son_on:
        print("ID:", record["id"])
        print("Tarix:", record["date_time"])
        print("Novu:", record["type"])
        
        if record["other_account"] != None:
            if record["type"] == "Transfer Sent":
                print("Alan hesab:", record["other_account"])
            else:
                print("Gonderen hesab:", record["other_account"])
                
        print("Mebleg:", format_money(record["amount"]), "AZN")
        
        if record["fee"] > 0:
            print("Komissiya:", format_money(record["fee"]), "AZN")
            
        print("Evvelki balans:", format_money(record["balance_before"]), "AZN")
        print("Sonraki balans:", format_money(record["balance_after"]), "AZN")
        print("-----------------------------------")


if __name__ == "__main__":
    print("Baza yuklenir ve qovluq yoxlanilir...")
    my_data = load_data()
    print("UGURLU! Qovluq ve 'users.json' fayli hazirdir.")