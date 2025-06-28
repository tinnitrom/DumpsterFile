import sqlite3
from random import randint
import base64

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
    do("DROP TABLE IF EXISTS user")
    do("DROP TABLE IF EXISTS posts")
    do("DROP TABLE IF EXISTS forums")
    
def create():
    open_db()
    curs.execute("PRAGMA foreign_keys= on")
    do("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY,
        login VARCHAR,
        password VARCHAR,
        photo BLOB)
        """)
    do("""CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY,
        id_user VARCHAR,
        user_name VARCHAR,
        photo BLOB,
        forum VARCHAR,
        content VARCHAR)
        """)
    do("""CREATE TABLE IF NOT EXISTS forums(
        id INTEGER PRIMARY KEY,
        id_user VARCHAR,
        name VARCHAR)
        """)
    close()
    
def add_user(user): 
    photo = user["image"].read()
    open_db() 
    curs.execute("INSERT INTO user (login, password, photo) VALUES (?,?,?)", 
                (user["login"],user["password"],photo)) 
    conn.commit() 
    close()

def get_forums():
    open_db()
    curs.execute("SELECT id, name FROM forums")
    rows = curs.fetchall()  # [('zz',), ('5z',)]
    close()
    return rows


def add_post(forum,content,user_id):
    open_db()
    user_name = get_user_by_id(user_id)
    photo = get_user_photo(user_id)
    curs.execute("INSERT INTO posts (id_user, user_name,photo, forum, content) VALUES (?,?,?,?,?)", 
                (user_id,user_name,photo,forum[0],content))
    print(get_user_photo_way(user_id))
    conn.commit()
    close()


def get_user_by_id(user_id):
    curs.execute("SELECT login FROM user WHERE id == (?)", (user_id,))
    user = curs.fetchone()
    return user[0]
def get_user_photo(user_id):
    curs.execute("SELECT photo FROM user WHERE id == (?)", (user_id,))
    user = curs.fetchone()
    return user[0]

    
def get_posts(forum):
    open_db()
    curs.execute("SELECT user_name, content, photo FROM posts WHERE forum == (?)", (forum,))
    rows = curs.fetchall() 
    close()
    result = []
    for user_name, content, photo in rows:
        if photo:
            photo_base64 = base64.b64encode(photo).decode('utf-8')
        else:
            photo_base64 = None
        result.append((user_name, content, photo_base64))

    return result
def get_user_photo_way(user_id):
    curs.execute("SELECT photo FROM user WHERE id = ?", (user_id,))
    result = curs.fetchone()
    if result and result[0]:
        encoded = base64.b64encode(result[0]).decode('utf-8')
        
        return encoded
    return None


# user1 = {
#         "id_user": 1,
#         "name": "zz"
#     }
# user2 = {
#         "id_user": 2,
#         "name": "5z"
#     }
def add_forums(forums): 
    open_db()
    print(forums["name"])
    curs.execute("SELECT id FROM forums WHERE name == (?)",
                 [str(forums["name"])])
    if curs.fetchone() == None:
        print(1)
        curs.execute("INSERT INTO forums (id_user, name) VALUES (?,?)", 
                    (forums["id_user"],forums["name"]))
        conn.commit() 
        curs.execute("SELECT id FROM forums WHERE id_user == (?) AND name == (?)",
                    [str(forums["id_user"]),str(forums["name"])])
        id = curs.fetchone()
        create_forum_page(forums['name'], id[0])
        close()
        return True
    else:
        return None 
    
def create_forum_page(name, index):
    with open("template/forum.html", "r") as template_file:
        html_content = template_file.read()
    with open(f"template/forums/forum-page-{name}-{index}.html", "w") as file:
        file.write(html_content)
def read_forum(forum_id):
    open_db()
    curs.execute("SELECT name FROM forums WHERE id == (?)",
                 (forum_id,))
    forum_name = curs.fetchone()
    return forum_name

    
    
def get_user(login, password):
    open_db()
    curs.execute("SELECT id, login FROM user WHERE login = ? AND password = ?", (login, password))
    result = curs.fetchone()
    close()
    return result

def run():
    clear_db()
    create()


if __name__ == "__main__":
    run()
