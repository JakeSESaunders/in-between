import sqlite3

# TODO be consistent with where string conversions take place

class User:
    def __init__(self, address, user_id):
        self.address = address
        self.user_id = user_id
        self.name = get_name(user_id)

def get_buddy_list(user_id):
    conn = sqlite3.connect('funkeys.sqlite3')
    c = conn.cursor()

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