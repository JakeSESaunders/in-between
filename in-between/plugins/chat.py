from plugins.plugin import Plugin
from data.user import get_name
from xml.etree.ElementTree import Element

import data.chat as chat

chat_rooms = {
    '1': chat.ChatRoom(),
    '2': chat.ChatRoom(),
    '3': chat.ChatRoom(),
    '4': chat.ChatRoom()
}

# TODO this whole thing is really messy
class PluginChat(Plugin):
    def __init__(self, plugin_id):
        Plugin.__init__(self, plugin_id)
        self.register_route('jn', self.handle_jn)
        self.register_route('lv', self.handle_lv)
        self.register_route('pj', self.handle_pj)
        self.register_route('ms', self.handle_ms)
        self.register_route('pd', self.handle_pd)
        self.register_route('of', self.handle_of)
        self.register_route('on', self.handle_on)
        self.register_route('se', self.handle_se)
        self.register_route('cr', self.handle_cr)
        self.register_route('cd', self.handle_cd)
        self.register_route('cp', self.handle_cp)
        self.register_route('ko', self.handle_ko)
        self.register_route('p', self.handle_p)

    def handle_jn(self, request):
        # TODO on join supply the player list
        # Example data <jn t="3"><pr dl="0| | " f="000000CD" uid="2734650" n="TEST" /></jn>
        #  bytearray(b'<jn t="3"><pr dl="0| | " f="000000CD" uid="3" n="TEST" /></jn>2|2|2|0#')
        # t is 0 for crib, 1 for gabby, 2 for rom, 3 for holler, 4 for rewind
        """Join"""
        t = request.get('t') # room type
        pr = request.find('pr')
        dl = pr.get('dl')
        f = pr.get('f') # av, funkey type
        uid = pr.get('uid') # user id
        n = pr.get('n') # login name

        self.user_id = uid

        r = '0' # TODO change this depending on circumstances, rather than just not returning anything
        plugin_id = '0' # NOTE this is something slightly different to plugin id

        response = Element('jn')
        response.set('r', r)
        response.set('id', plugin_id) # NOTE not the user id

        chat_user = chat.ChatUser(uid, n, f, dl, self)

        global chat_rooms
        if chat_rooms[t].user_join(chat_user):
            return response
        
    def handle_lv(self, request):
        """Leave"""
        id = request.get('id') # NOTE not the user id
        t = request.get('t')

        response = Element('lv')

        global chat_rooms
        chat_rooms[t].user_disconnect(self.user_id)

        return response

    def handle_pj(self, request):
        """Player List/Join"""
        pass

    def handle_ms(self, request):
        """Message"""
        m = request.get('m')
        t = request.get('t')
        id = request.get('id')

        #name = self.user.name
        #name = 'TEST'
        #message = m

        #response = Element('ms')
        #response.set('n', name)
        #response.set('m', message)

        global chat_rooms
        chat_rooms[t].user_send_message(self.user_id, m)

    def handle_pd(self, request):
        """Player Remove"""
        pass

    def handle_of(self, request):
        """Player Disconnected"""
        pass

    def handle_on(self, request):
        """Player Connected"""
        pass

    def handle_se(self, request):
        """Special Event"""
        # On receiving a special event, broadcast to all other chat room users
        room_id = request.get('t')
        chat_rooms[room_id].send_to_room(request)
        return request

        #event = request[0]
        #event_id = event.tag

        #response = Element('se')
        # there are several special events that need to be handled with ids:
        # pl (player join) a="1" id="1" s="c" n="13:12"
        # cr
        # mv (Move)
        #if event_id == 'mv':
        #    user_id = event.get('id')
        #    s = event.get('s')
        #    n = event.get('c')
        # od (moving to a different room in crib)
        # ia (interact with item)
        # pi (place item)
        # ri (remove item)
        
        # return response

    def handle_cr(self, request):
        """Create Room"""
        pass

    def handle_cd(self, request):
        """Creator Disconnect (Leave Crib)"""
        pass

    def handle_cp(self, request):
        """Player Properties?""" # changes the funkey
        pass

    def handle_ko(self, request):
        """Kick Out"""
        pass

    def handle_p(self, request):
        """Ping"""
        # TODO use to send client 'waiting messages'