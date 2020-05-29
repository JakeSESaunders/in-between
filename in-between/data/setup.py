import sqlite3
from settings import db_path

def setup_database():
    # TODO check if database already exists
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE base_user(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            question TEXT,
            answer TEXT,
            bf INTEGER,
            cf INTEGER,
            ph INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE user_buddy(
            relation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_id INTEGER,
            to_id INTEGER,
            status INTEGER,
            FOREIGN KEY(from_id) REFERENCES base_user(user_id),
            FOREIGN KEY(to_id) REFERENCES base_user(user_id)
        )
    ''')
    # TODO assert some of these values not null, or discount 0/1
    c.execute('''
        CREATE TABLE trunk_jammers(
            stack_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT,
            quantity INTEGER,
            cost INTEGER,
            discount INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE trunk_familiars(
            stack_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT,
            time INTEGER,
            cost INTEGER,
            discounted_cost INTEGER,
            discount INTEGER
        )
    ''')
    conn.commit()
    conn.close()