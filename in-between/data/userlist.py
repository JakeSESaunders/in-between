class UserList:
    def __init__(self):
        self.users = []

    def user_connect(self, user):
        """Adds given user to client list."""
        if self.get_user(user.id) == None:
            self.users.append(user)

    def user_disconnect(self, user_id):
        """Removes given user from client list."""
        users_to_remove = []
        for user in self.users:
            if user.user_id == user_id:
                users_to_remove.append(user)
        for user in users_to_remove:
            self.users.remove(user)

    def get_user(self, user_id):
        """Returns user with id user_id."""
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def send_to_user(self, user_id):
        pass