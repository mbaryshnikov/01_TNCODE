import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def json_open(f):
    with open(BASE_DIR / "data" / f, 'r', encoding='utf-8') as f:
        return json.load(f)


def db_writer(data, f):
    conn = sqlite3.connect(BASE_DIR / "data" / f)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM speisekarte")
    with conn:
        for k, v in data.items():
            sql = "INSERT INTO speisekarte (ID, partition, title, pries) Values (:dish_num, :partition, :title, :pries);"
            cursor.execute(sql, v)
    conn.close()


def main():
    sk = json_open('speisekarte.json')
    db_writer(sk, 'restaurant.db')


if __name__ == '__main__':
    main()