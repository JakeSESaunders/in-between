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
        # TODO return correct error codes
        if self.get_user_from_id(user_id) is None:
            # set up chatuser
            joining_user = Chatuser(user_id, name, funkey_id, dl, handler)

            response_code = '0'

            # send user list and make users appear for joining user
            xml_join_message = Element('jn')
            xml_join_message.set('r', response_code)
            joining_user.send(xml_join_message)

            xml_userlist = Element('pj')
            xml_show_all_users = Element('se')
            for user in self.users:
                xml_user = Element('pr')
                xml_user.set('uid', str(user.user_id))
                xml_user.set('n', user.name)
                xml_user.set('f', user.funkey_id)
                xml_user.set('dl', user.dl)
                xml_userlist.append(xml_user)

                xml_show_user = Element('pl')
                xml_show_user.set('id', str(user.user_id))
                xml_show_user.set('n', '13:12')
                xml_show_user.set('s', 'c')
                xml_show_user.set('a', '1')
                xml_show_all_users.append(xml_show_user)
            joining_user.send(xml_userlist)
            joining_user.send(xml_show_all_users)

            self.users.append(joining_user)

            # send joining user and make joining user appear for present users
            xml_player_data = Element('pr')
            xml_player_data.set('uid', str(joining_user.user_id))
            xml_player_data.set('n', joining_user.name)
            xml_player_data.set('f', joining_user.funkey_id)
            xml_player_data.set('dl', joining_user.dl)

            xml_player_join = Element('pj')
            xml_player_join.append(xml_player_data)
            
            self.send_to_room(int(joining_user.user_id), xml_player_join)

            xml_show_player = Element('pl')
            xml_show_player.set('id', str(joining_user.user_id))
            xml_show_player.set('n', '13:12')
            xml_show_player.set('s', 'c')
            xml_show_player.set('a', '1')

            xml_show_player_container = Element('se')
            xml_show_player_container.append(xml_show_player)

            self.send_to_room(int(joining_user.user_id), xml_show_player_container)

    def disconnect(self, user_id):
        """Removes user with given id from user list."""
        xml_leave = Element('pd')
        xml_leave.set('id', str(user_id))

        for user in self.users:
            if user.user_id == user_id:
                self.send_to_room(int(user_id), xml_leave)
                self.users.remove(user)
                

    def send_to_room(self, user_id, xml_message):
        """Send an xml message to all users in the room (except the user with given id, who supplied the message)."""
        for user in self.users:
            if user.user_id != user_id:
                user.send(xml_message)