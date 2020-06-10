from data.user.userlist import Userlist
from data.chat.chatrooms import Chatrooms
from data.chat.chatroom import Chatroom

# File for data structures which need not be saved to a database

userlist = Userlist()

chatrooms = Chatrooms()
# NOTE room id 0 is for cribs
chatrooms.add_room(Chatroom(0)) # Test Crib
chatrooms.add_room(Chatroom(1)) # Gabby
chatrooms.add_room(Chatroom(2)) # Rom
chatrooms.add_room(Chatroom(3)) # Holler
chatrooms.add_room(Chatroom(4)) # Rewind