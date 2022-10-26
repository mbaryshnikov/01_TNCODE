"""
Hauptprogramm
"""
import sqlite3
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


def db_reader(f):
    conn = sqlite3.connect(BASE_DIR / "data" / f)
    cursor = conn.cursor()
    sql = "SELECT * FROM speisekarte;"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    sk_dict = {}
    for _ in results:
        sk_dict[str(_[0])] = {
            "partition": _[1],
            "dish_num": _[0],
            "title": _[2],
            "pries": _[3]
            }
    return sk_dict


def sk_printen():
    sk = db_reader('restaurant.db')
    for k, v in sk.items():
         print(f'{k} {v["partition"]} {v["title"]} {v["pries"]}€')


def receipt_lst(lst, d, cust, n):
    s = 0
    sk = db_reader('restaurant.db')
    rcpt_lst = []
    rcpt_lst.append('*' * 32 )
    rcpt_lst.append('ACASA Restaurant')
    rcpt_lst.append(f'Your receipt N_{n} {d}:')
    rcpt_lst.append(f'Customer Id:{cust[0]} Name: {cust[1]} {cust[2]}')
    rcpt_lst.append('-' * 32 )
    for _ in lst:
        if _ in sk:
            rcpt_lst.append(f'{_} {sk[_]["partition"]} {sk[_]["title"]} {sk[_]["pries"]}€')
            s += int(sk[_]["pries"])
        else:
            rcpt_lst.append('000 wrong entry')
    rcpt_lst.append(f'Total {s}€')
    rcpt_lst.append('Thanks a lot for your visit!')
    return rcpt_lst


def receipt_save(lst):
    with open(BASE_DIR / "data" / "receipt_log.txt", 'a', encoding='utf-8') as f:
        for _ in lst:
            print(_, file=f)


def customer_input(f):
    conn = sqlite3.connect(BASE_DIR / "data" / f)
    cursor = conn.cursor()
    with conn:
        us_in = [input(f'Input {_}: ') for _ in ('First Name', 'Last Name', 'Tel')]
        sql = "SELECT * FROM Customer WHERE First_Name = '" + us_in[0] + "' and Last_Name = '" +us_in[1]+"';"
        cursor.execute(sql)
        results = cursor.fetchone()
        if results is None:
            sql = "INSERT INTO Customer (First_Name, Last_Name, Tel) Values (?, ?, ?);"
            cursor.execute(sql, us_in)
            sql = "SELECT * FROM Customer WHERE First_Name = '" + us_in[0] + "' and Last_Name = '" +us_in[1]+"';"
            cursor.execute(sql)
            results = cursor.fetchone()
    conn.close()
    return results


def order_saver(id, my_list, d, f):
    conn = sqlite3.connect(BASE_DIR / "data" / f)
    cursor = conn.cursor()
    with conn:
        sql = "INSERT INTO Orders (ID_Customer, Order_lst, D_T) VALUES (?, ?, ?);"
        cursor.execute(sql, (int(id), my_list, d))
        sql = "SELECT COUNT(*) FROM Orders"
        cursor.execute(sql)
        cnt = cursor.fetchone()[0]
    conn.close()
    return cnt


def main():
    d = datetime.now().strftime("%d.%m.%y %H:%M")
    print('*' * 32 )
    print('Willkommen bei Acasa Restaurant!')
    customer = customer_input('restaurant.db')
    print('*' * 32 )
    sk_printen()
    order_list=[]
    while True:
        user_input = input('What would you like? (0 - exit) >>')
        if user_input != '0':
            order_list.append(user_input)
        else:
            break
    RSPT_COUNT = order_saver(customer[0], ','.join(order_list), d, 'restaurant.db')
    rcpt_lst = receipt_lst(order_list, d, customer, RSPT_COUNT)
    print(*rcpt_lst, sep='\n')
    receipt_save(rcpt_lst)


if __name__ == '__main__':
    main()
    