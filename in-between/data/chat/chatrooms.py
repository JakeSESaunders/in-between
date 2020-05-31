class Chatrooms:
    def __init__(self):
        self.rooms = {}

    def add_room(self, chatroom):
        self.rooms[chatroom.room_id] = chatroom

    def get_room(self, room_id):
        return self.rooms[room_id]