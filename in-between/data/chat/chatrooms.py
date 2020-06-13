class Chatrooms:
    def __init__(self):
        self.rooms = {}

    def add_room(self, chatroom):
        self.rooms[chatroom.room_id] = chatroom

    def get_room(self, room_id):
        return self.rooms[room_id]

    def disconnect(self, user_id):
        """Disconnect user with given id from all chat rooms"""
        for room_id in self.rooms.keys():
            self.rooms[room_id].disconnect(user_id)