"""
Hauptprogramm
"""
import sqlite3
import pandas as pd
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
    sql = f"SELECT Cars.ID, m.Producer, m.Model, m.Class, m.Price FROM Cars JOIN Colors as 'c' on c.ID = Cars.Color\
        JOIN Models as 'm' on m.ID = Cars.Model JOIN Status as 's' on s.ID = Cars.Status WHERE Avl = {stat} ORDER BY m.Producer;"
    lst = db_exec('europcar.db', sql)
    columns = ('ID', 'Produser', 'Model', 'Class', 'Price')
    print('-' * 38)
    df = pd.DataFrame(lst, columns=columns)
    print (df)
    print('-' * 38)
    return lst


def main():
    print('-' * 38)
    print('Welcome by Europcar!')
    print('avaiable cars:')
    cars_list = cars_print(1) # 1 - availabl
    user_ch = int(input('User_Wish ID: '))
    user_ch = [x for x in cars_list if x[0] == user_ch][0]
    if user_ch == []:
        print('There is no such car!')
    else:
        user_days = int(input('For how many days: '))
        print(f'Your rent will be: {float(user_ch[4]) * int(user_days):.2f}$ ')
        sql = f"UPDATE Cars SET Status = 2 WHERE ID = {user_ch[0]};"
        db_exec('europcar.db', sql)


if __name__ == '__main__':
    main()
    