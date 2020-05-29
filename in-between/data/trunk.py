import sqlite3
from settings import db_path

class Jammer:
    def __init__(self, stack_id, item_id, quantity, cost, discount):
        self.stack_id = stack_id
        self.item_id = item_id
        self.quantity = quantity
        self.cost = cost
        self.discount = discount

class Familiar:
    def __init__(self, stack_id, item_id, time, cost, discounted_cost, discount):
        self.stack_id = stack_id
        self.item_id = item_id
        self.time = time
        self.cost = cost
        self.discounted_cost = discounted_cost
        self.discount = discount

def get_jammer_list():
    """Returns a list of jammer data for display in the trunk."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT * FROM trunk_jammers
    ''')
    raw_jammer_data = c.fetchall()
    conn.close()

    jammer_list = []
    for jammer_data in raw_jammer_data:
        stack_id = str(jammer_data[0])
        item_id = str(jammer_data[1])
        quantity = str(jammer_data[2])
        cost = str(jammer_data[3])
        discount = str(jammer_data[4])
        jammer_list.append(Jammer(stack_id, item_id, quantity, cost, discount))

    return jammer_list

def get_familiar_list():
    """Returns a list of familiar data for display in the trunk."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT * FROM trunk_familiars
    ''')
    raw_familiar_data = c.fetchall()
    conn.close()

    familiar_list = []
    for familiar_data in raw_familiar_data:
        stack_id = str(familiar_data[0])
        item_id = str(familiar_data[1])
        time = str(familiar_data[2])
        cost = str(familiar_data[3])
        discounted_cost = str(familiar_data[4])
        discount = str(familiar_data[5])
        familiar_list.append(Familiar(stack_id, item_id, time, cost, discounted_cost, discount))

    return familiar_list