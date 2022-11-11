import sqlite3

db = sqlite3.connect('new2.db')
cur = db.cursor()


async def db_conn():
    cur.execute("CREATE TABLE IF NOT EXISTS users_flag (user_id INTEGER PRIMARY KEY, flag TEXT)")

    db.commit()


async def new_user(user_id):
    cur.execute("INSERT INTO users_flag (user_id) VALUES(?)", (user_id,))
    db.commit()


async def insert_eng(user_id):
    cur.execute("INSERT INTO users_flag (flag) VALUES(?) WHERE user_id = ?", ('eng', user_id,))
    db.commit()


async def update_ru(user_id):
    cur.execute("UPDATE users_flag SET flag = ? WHERE user_id = ?", ('ru', user_id,))
    db.commit()


async def update_eng(user_id):
    cur.execute("UPDATE users_flag SET flag = ? WHERE user_id = ?", ('eng', user_id,))
    db.commit()


async def sel_lang(user_id):
    x = cur.execute("SELECT flag FROM users_flag WHERE user_id = ?", (user_id,)).fetchone()
    return str(x)