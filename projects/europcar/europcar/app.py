"""
Hauptprogramm
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def db_exec(f, st):
    conn = sqlite3.connect(BASE_DIR / "data" / f)
    cursor = conn.cursor()
    with conn:
        cursor.execute(st)
        results = cursor.fetchall()
    conn.close()
    return results


def cars_print(stat):
    sql = f"SELECT Cars.ID, m.Producer, m.Model, m.Class, m.Price FROM Cars JOIN Colors as 'c' on c.ID = Cars.Color JOIN Models as 'm' on m.ID = Cars.Model JOIN Status as 's' on s.ID = Cars.Status WHERE Avl = {stat} ORDER BY m.Producer;"
    lst = db_exec('europcar.db', sql)
    print('-' * 38)
    print(' N Produser     Model   Class   Price')
    print('-' * 38)
    [print(f' {_[0]} {_[1]:10}\t{_[2]}\t{_[3]}\t{_[4]}\t') for _ in lst]
    return lst


def main():
    d = datetime.now().strftime("%d.%m.%y %H:%M")
    print('*' * 32 )
    print('Welcome by Europcar!')
    print('avaiable cars:')
    cars_list = cars_print(1)
    user_ch = int(input('User_Wish: '))
    user_ch = [x for x in cars_list if x[0] == user_ch]
    if user_ch == []:
        print('There is no such car!')
    else:
        user_days = int(input('For how many days: '))
        print(f'Your rent will be: {float(user_ch[0][4]) * int(user_days):.2f}$ ')
        sql = f"UPDATE Cars SET Status = 2 WHERE ID = {user_ch[0][0]};"
        db_exec('europcar.db', sql)


if __name__ == '__main__':
    main()
    