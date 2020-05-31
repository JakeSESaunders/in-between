from data.chat.chatuser import Chatuser
from xml.etree.ElementTree import Element

class Chatroom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.users = []

    def get_user_from_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def connect(self, user_id, name, funkey_id, dl, handler):
        """Adds given user to user list."""
        if self.get_user_from_id(user_id) is None:
            user = Chatuser(user_id, name, funkey_id, dl, handler)
            self.users.append(user)

            # TODO send user list back to user

            xml_player = Element('pr')
            xml_player.set('uid', str(user.user_id))
            xml_player.set('n', user.name)
            xml_player.set('f', user.funkey_id)
            xml_player.set('dl', user.dl)

            xml_join = Element('pj')
            xml_join.append(xml_player)

            self.send_to_room(user_id, xml_join)

            xml_show = Element('pl')
            xml_show.set('id', str(user.user_id))
            xml_show.set('n', '13:12')
            xml_show.set('s', 'c')
            xml_show.set('a', '1')

            xml_se = Element('se')
            xml_se.append(xml_show)

            self.send_to_room(user_id, xml_se)

            return True
        return False

    def disconnect(self, user_id):
        """Removes user with given id from user list."""
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
                # TODO send player disconnect

    def send_to_room(self, user_id, xml_message):
        """Send an xml message to all users in the room (except the user with given id, who supplied the message)."""
        for user in self.users:
            if user.user_id != user_id:
                user.send(xml_message)