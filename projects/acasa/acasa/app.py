"""
Hauptprogramm
"""
import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

def json_open(f):
    with open(BASE_DIR / "data" / f, 'r', encoding='utf-8') as f:
        return json.load(f)    


def sk_printen():
    sk = json_open('speisekarte.json')
    for k, v in sk.items():
         print(f'{k} {v["partition"]} {v["title"]} {v["pries"]}€')


def receipt_lst(lst):
    s = 0
    sk = json_open('speisekarte.json')
    rcpt_lst = []
    rcpt_lst.append('*' * 32 )
    current_dt = datetime.now()
    rcpt_lst.append('ACASA Restaurant')
    rcpt_lst.append(f'Your receipt N_{RSPT_COUNT} {current_dt.strftime("%d.%m.%y %H:%M")}:')
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


def count_reader():
    try:
        with open(BASE_DIR / "data" / 'count.txt', 'r', encoding='utf-8') as f:
            return int(f.read().strip())
    except:
         print('ja sdes')
         return 0


def count_saver():
    with open(BASE_DIR / "data" / 'count.txt', 'w', encoding='utf-8') as f:
        print(RSPT_COUNT, file=f)


def main():
    global RSPT_COUNT
    RSPT_COUNT = count_reader()
    print('*' * 32 )
    print('Willkommen bei Acasa Restaurant!')
    print('*' * 32 )
    sk_printen()
    order_list=[]
    while True:
        user_input = input('What would you like? (0 - exit) >>')
        if user_input != '0':
            order_list.append(user_input)
        else:
            break
    RSPT_COUNT += 1
    count_saver()
    rcpt_lst = receipt_lst(order_list)
    print(*rcpt_lst, sep='\n')
    receipt_save(rcpt_lst)


if __name__ == '__main__':
    main()