from plugins.plugin import Plugin
from xml.etree.ElementTree import Element

from data.volatile import chatrooms

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
        self.user_id = None
        self.name = None

    def handle_jn(self, request):
        """Join"""
        room_id = int(request.get('t'))
        player = request.find('pr')
        user_id = int(player.get('uid'))
        name = player.get('n')
        funkey_id = player.get('f')
        dl = player.get('dl')
        
        self.user_id = user_id
        self.name = name

        global chatrooms
        connected = chatrooms.get_room(room_id).connect(user_id, name, funkey_id, dl, self)

        if connected:
            r = '0' # 0: OK, 1: closed for cleaning, 2: closed for cleaning
            plugin_id = '0'
            response = Element('jn')
            response.set('r', r)
            response.set('id', plugin_id)

            return response
        
    def handle_lv(self, request):
        """Leave"""
        id = request.get('id') # NOTE not the user id, figure out what this is
        room_id = int(request.get('t'))

        response = Element('lv')

        global chatrooms
        chatrooms.get_room(room_id).disconnect(self.user_id)

        return response

    def handle_pj(self, request):
        """Player List/Join"""
        pass

    def handle_ms(self, request):
        """Message"""
        m = request.get('m')
        room_id = int(request.get('t'))
        id = request.get('id')

        name = self.name
        message = m

        response = Element('ms')
        response.set('n', name)
        response.set('m', message)

        global chatrooms
        chatrooms.get_room(room_id).send_to_room(self.user_id, response)

        return response

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
        room_id = int(request.get('t'))
        global chatrooms
        chatrooms.get_room(room_id).send_to_room(self.user_id, request)

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