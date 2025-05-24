import sqlite3
from random import randint

conn = None
curs = None

def open_db():
    global conn, curs
    conn = sqlite3.connect('users_database.sqlite')
    curs = conn.cursor()

def close():
    curs.close()
    conn.close()
    
def do(request):
    curs.execute(request)
    conn.commit()
    
def clear_db():
    open_db()
    do("DROP TABLE IF EXISTS quiz_content")
    do("DROP TABLE IF EXISTS quiz")
    do("DROP TABLE IF EXISTS question")
    do("DROP TABLE IF EXISTS user")
    
def create():
    open_db()
    curs.execute("PRAGMA foreign_keys= on")
    do("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY,
        login VARCHAR,
        name VARCHAR,
        password VARCHAR,
        about VARCHAR,
        photo BLOB)
        """)
    close()
    
def add_user(user): 
    print(user["image"])
    photo = user["image"].read()
    open_db() 
    curs.execute("INSERT INTO user (login, name, password, about, photo) VALUES (?,?,?,?,?)", 
                (user["login"],user["name"],user["password"],user["about"],photo)) 
    conn.commit() 
    close()
    
def get_user(login, password):
    open_db()
    # curs.execute("SELECT id, login FROM user WHERE login==(?) AND password==(?)", (login, password))
    curs.execute("SELECT id, login FROM user WHERE login = ? AND password = ?", (login, password))
    result = curs.fetchone()
    close()
    return result

def run():
    clear_db()
    create()


if __name__ == "__main__":
    run()

