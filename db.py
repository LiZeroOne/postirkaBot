import sqlite3


def create_table():
    conn = sqlite3.connect('postirka.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       userid INT PRIMARY KEY,
       name TEXT,
       room INT);
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS records(
       date TEXT,
       userid TEXT);
    """)
    conn.commit()

    conn.close()


def insert_user(data):
    conn = sqlite3.connect('postirka.db')
    cur = conn.cursor()

    cur.execute("INSERT OR REPLACE INTO users VALUES(?, ?, ?);", data)
    conn.commit()

    # Проверяем результат
    cur.execute("SELECT * FROM users ORDER BY userid LIMIT 3")
    results = cur.fetchall()
    print(results)

    conn.close()


def insert_record(data):
    conn = sqlite3.connect('postirka.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO records VALUES(?, ?);", data)
    conn.commit()

    cur.execute("SELECT * FROM records ORDER BY userid LIMIT 3")
    results = cur.fetchall()
    print(results)

    conn.close()
