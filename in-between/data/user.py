import sqlite3

class User:
    def __init__(self, handler, user_id):
        self.handler = handler
        self.user_id = user_id
        self.name = get_name(user_id)

def get_buddy_list(user_id):
    conn = sqlite3.connect('funkeys.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT to_id
        FROM user_buddy
        WHERE from_id == :user_id
    ''', {
        'user_id': user_id
    })
    from_buddy = c.fetchall()
    c.execute('''
        SELECT from_id
        FROM user_buddy
        WHERE to_id == :user_id
    ''', {
        'user_id': user_id
    })
    to_buddy = c.fetchall()
    conn.close()
    buddies = to_buddy + from_buddy
    for buddy in buddies:
        buddy_ids.append(buddy[0])
    buddy_ids = []

def check_login(name, password):
    conn = sqlite3.connect('funkeys.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT *
        FROM base_user
        WHERE name == :name
    ''', {
        'name': name
    })
    user = c.fetchone()
    conn.close()
    if user[2] == password:
        return str(user[0])
    return None

def get_name(user_id):
    conn = sqlite3.connect('funkeys.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT name
        FROM base_user
        WHERE user_id == :user_id
    ''', {
        'user_id': user_id
    })
    name = c.fetchone()
    conn.close()
    return name[0]

def register_user(name, password, question, answer):
    """Register a user to the database and return the new user's id."""
    # TODO check name isn't reserved etc.
    # TODO check table has been setup
    conn = sqlite3.connect('funkeys.sqlite3')
    c = conn.cursor()
    c.execute('INSERT INTO base_user (name, password, question, answer) VALUES (:name, :password, :question, :answer)', {
        'name': name,
        'password': password,
        'question': question,
        'answer': answer
    })
    user_id = str(c.lastrowid)
    conn.commit()
    conn.close()

    return user_id