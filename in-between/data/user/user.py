import sqlite3
from settings import db_path

class User:
    # handler is the base request handler
    def __init__(self, user_id, handler):
        details = get_user_details(user_id)
        self.user_id = details[0]
        self.name = details[1]
        self.online = 1 # NOTE redundant, any connected user has online status 1
        self.status = 0
        self.bf = details[2]
        self.cf = details[3]
        self.ph = details[4]
        self.handler = handler

    def send(self, response, plugin_id=None):
        """Send an xml message directly to the user connected at the given address."""
        if plugin_id is None:
            self.handler.send_response(response)
        else:
            # TODO check plugin with id exists
            self.handler.plugins[plugin_id].queue_response(response)

    def add_buddy(self, buddy_id):
        """Create a buddy relation between this user and the user with the given id."""
        # TODO make idempotent
        if get_name(buddy_id) is None:
            return
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO user_buddy (from_id, to_id, status)
            VALUES (:from_id, :to_id, 0)
        ''', {
            'from_id': int(self.user_id),
            'to_id': int(buddy_id)
        })
        conn.commit()
        conn.close()

    def delete_buddy(self, buddy_id):
        """Delete all buddy relations between this user and the user with the given id."""
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            DELETE FROM user_buddy
            WHERE (from_id == :user_id AND to_id == :buddy_id) OR (from_id == :buddy_id AND to_id == :user_id)
        ''', {
            'user_id': self.user_id,
            'buddy_id': self.buddy_id
        })
        conn.commit()
        conn.close()

    def get_buddy_ids(self):
        """Returns a list of the ids of the user's buddies."""
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            SELECT from_id
            FROM user_buddy
            WHERE to_id == :to_id
        ''', {
            'to_id': self.user_id
        })
        from_buddy_ids = c.fetchall()
        c.execute('''
            SELECT to_id
            FROM user_buddy
            WHERE from_id == :from_id
        ''', {
            'from_id': self.user_id
        })
        to_buddy_ids = c.fetchall()
        conn.close()
        buddy_ids = from_buddy_ids + to_buddy_ids
        return [buddy_id[0] for buddy_id in buddy_ids]

def register(name, password, question, answer): # TODO
    """Register a user with the given credentials. Returns the user id. If user with the given name already exists, return None."""
    if get_id(name) is not None:
        return None
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO base_user (name, password, question, answer, bf, cf, ph)
        VALUES (:name, :password, :question, :answer, :bf, :cf, :ph)
    ''', {
        'name': name,
        'password': password,
        'question': question,
        'answer': answer,
        'bf': 0,
        'cf': 0,
        'ph': 0
    })
    c.execute('''
        SELECT user_id
        FROM base_user
        WHERE name == :name
    ''', {
        'name': name
    })
    user_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return user_id

def login(name, password):
    """Login a user with the given credentials. Returns the user id. If user not found or password incorrect, return None."""
    # check if user exists
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT user_id, password
        FROM base_user
        WHERE name == :name
    ''', {
        'name': name
    })
    user_details = c.fetchone()
    conn.close()
    if user_details is not None:
        if password == user_details[1]:
            return user_details[0]
    return None

def get_id(name):
    """Return the id of the user with given name. If user not found, return None."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT user_id
        FROM base_user
        WHERE name == :name
    ''', {
        'name': name
    })
    user_id = c.fetchone()
    conn.close()
    if user_id is not None:
        return user_id[0]

def get_name(user_id):
    """Return the name of the user with given id. If user not found, return None."""
    conn = sqlite3.connect(db_path)
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
    if name is not None:
        return name[0]

def get_user_details(user_id):
    """Get the details of the user with given id. Returns a tuple. Returns None if user not found."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT user_id, name, bf, cf, ph
        FROM base_user
        WHERE user_id == :user_id
    ''', {
        'user_id': user_id
    })
    user_details = c.fetchone()
    conn.close()
    return user_details