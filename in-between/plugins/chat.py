from plugins.plugin import Plugin
from xml.etree.ElementTree import Element

# TODO reimplement this as some kind of 'user volatile data storage'
isInChatSession = False

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
        # Example data <jn t="3"><pr dl="0| | " f="000000CD" uid="2734650" n="TEST" /></jn>
        """Join"""
        t = request.get('t') # room type
        pr = request.find('pr')
        dl = pr.get('dl')
        f = pr.get('f') # av, funkey type
        uid = pr.get('uid') # user id
        n = pr.get('n') # login name

        r = '0'
        plugin_id = '0' # NOTE this is something slightly different to plugin id

        response = Element('jn')
        response.set('r', r)
        response.set('id', plugin_id)

        global isInChatSession
        if not isInChatSession: 
            isInChatSession = True
            return response
        return None
        
    def handle_lv(self, request):
        """Leave"""
        id = request.get('id')
        t = request.get('t')

        response = Element('lv')

        global isInChatSession
        if isInChatSession: 
            isInChatSession = False
            return response
        return None

    def handle_pj(self, request):
        """Player List/Join"""
        pass

    def handle_ms(self, request):
        """Message"""
        m = request.get('m')
        t = request.get('t')
        id = request.get('id')

        name = 'TEST'
        message = m

        response = Element('ms')
        response.set('n', name)
        response.set('m', message)

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
        event = request[0]
        event_id = event.tag

        response = Element('se')
        # there are several special events that need to be handled with ids:
        # pl
        # cr
        # mv (Move)
        if event_id == 'mv':
            user_id = event.get('id')
            s = event.get('s')
            n = event.get('c')
        # od (moving to a different room in crib)
        # ia (interact with item)
        # pi (place item)
        # ri (remove item)
        
        return response

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