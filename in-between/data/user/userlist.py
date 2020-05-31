from data.user.user import User, get_id, get_name, login, get_user_details

class Userlist:
    def __init__(self):
        self.users = []

    def connect(self, user_id, handler):
        """Adds given user to user list. Return login code."""
        # 0 for OK, 2 for logged in from different address
        user_logged_in = self.get_user_from_id(user_id)
        if user_logged_in is not None:
            if handler.client_address[0] != user_logged_in.handler.client_address[0]:
                return 2
        new_user = User(user_id, handler)
        self.users.append(new_user)
        handler.plugins[1].set_user_id(user_id)
        # TODO send to all user's buddies that the user is online
        return 0

    def disconnect(self, user_id):
        """Removes user with given id from user list."""
        user = self.get_user_from_id(user_id)
        while user is not None:
            self.users.remove(user)
            user = self.get_user_from_id(user_id)

    def get_user_from_id(self, user_id):
        """Gets user with given id if user is connected to server. If not, return None."""
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_user_from_name(self, name):
        """Gets user with given name if user is connected to server. If not, return None."""
        user_id = get_id(name)
        if user_id is not None:
            return self.get_user_from_id(user_id)
        return None

    def send_to_user_id(self, user_id, message, plugin_id=None):
        """Send an xml message to user with given id. Returns True/False if user does/n't exist."""
        user = self.get_user_from_id(user_id)
        if user is not None:
            user.send(message, plugin_id)
            return True
        return False

    def send_to_user_name(self, name, message, plugin_id=None):
        """Send an xml message to user with given name. Returns True/False if user does/n't exist."""
        user_id = get_id(name)
        if user_id is not None:
            return send_to_user_id(user_id, message, plugin_id)
        return False

    def get_buddy_list(self, user_id):
        """Get the details of the buddies of the user with given id. Returns a list of tuples."""
        buddy_details = []
        user = self.get_user_from_id(user_id)
        if user is None:
            return []
        buddy_ids = user.get_buddy_ids()
        for buddy_id in buddy_ids:
            buddy = self.get_user_from_id(buddy_id)
            if buddy is not None:
                buddy_details.append((buddy.user_id, buddy.name, buddy.online, buddy.status, buddy.bf, buddy.cf, buddy.ph))
            else:
                buddy = get_user_details(buddy_id)
                buddy_details.append((buddy[0], buddy[1], 1, 0, buddy[2], buddy[3], buddy[4]))
        return buddy_details

    def change_chat_status(self, user_id, status):
        """Change the chat status of the user with specified id to the given status."""
        user = self.get_user_from_id(user_id)
        if user is not None:
            user.status = status