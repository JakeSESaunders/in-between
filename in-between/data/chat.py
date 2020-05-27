from xml.etree.ElementTree import Element

class ChatUser:
    def __init__(self, user_id, name, funkey_id, dl, chat_plugin):
        self.user_id = user_id
        self.name = name
        self.funkey_id = funkey_id
        self.dl = dl
        self.chat_plugin = chat_plugin

# TODO fix up the naming schemes a bit here; too much 'message'
class ChatRoom:
    def __init__(self):
        self.users = []

    def get_user(self, user_id):
        print(self.users)
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def user_join(self, chat_user):
        if self.get_user(chat_user.user_id) is None:
            self.users.append(chat_user)

            response = Element('pj')
            player = Element('pr')
            player.set('uid', chat_user.user_id)
            player.set('n', chat_user.name)
            player.set('f', chat_user.funkey_id)
            player.set('dl', chat_user.dl)
            response.append(player)

            self.send_to_room(response)

            return True
        return False

    def user_disconnect(self, user_id):
        users_to_remove = []

        for user in self.users:
            if user.user_id == user_id:
                users_to_remove.append(user)

        for user in users_to_remove:
            self.users.remove(user)

    def user_send_message(self, user_id, message):
        user = self.get_user(user_id)
        if user is not None:
            name = user.name

            response = Element('ms')
            response.set('n', name)
            response.set('m', message)

            self.send_to_room(response)

    def send_to_room(self, message):
        for user in self.users:
            user.chat_plugin.queue_response(message)