import sqlite3

def setup_database():
    conn = sqlite3.connect('funkeys.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE base_user(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            question TEXT,
            answer TEXT
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