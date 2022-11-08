import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

def db_exec(f, st):
    conn = sqlite3.connect(BASE_DIR / "data" / f)

    cursor = conn.cursor()
    with conn:
        cursor.execute(st)
        results = cursor.fetchall()
    conn.close()
    return results
