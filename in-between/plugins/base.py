from plugins.plugin import Plugin
from xml.etree.ElementTree import Element
from copy import copy

class PluginBase(Plugin):
    def __init__(self, plugin_id):
        Plugin.__init__(self, plugin_id)
        self.register_route('a_lru', self.handle_a_lru)
        self.register_route('a_lgu', self.handle_a_lgu)
        self.register_route('a_gsd', self.handle_a_gsd)
        self.register_route('a_gpd', self.handle_a_gpd)
        self.register_route('a_gsl', self.handle_a_gsl)
        self.register_route('a_gfl', self.handle_a_gfl)
        self.register_route('a_alo', self.handle_a_alo)
        self.register_route('p', self.handle_p)

    def get_responses(self):
        responses = copy(self.responses)
        self.responses = []
        return responses

    def handle_a_lru(self, request):
        request_login_code = request.get('l')
        name = request.get('n')
        password = request.get('p')

        service_id = '1' # NOTE arbitrary constant

        response = Element('a_lru')

        #user_id = check_login(name, password)
        #if user_id is not None:
        #    response_login_code = '0'
        #    response.set('u', user_id)
       # 
       #     client_address = self.client_address
       #     user = User(client_address, user_id)
       # else:
        #    response_login_code = '1'
            
        response_login_code = '0'
        service_id = '1'

        response.set('r', response_login_code)
        response.set('s', service_id)

        self.queue_response(response)

    def handle_a_lgu(self, request):
        affiliate_id = request.get('a')
        client_id = request.get('c')
        advertising_id = request.get('d')
        # NOTE purpose of this route is unknown, why are we providing a guest user with a password???
        response_login_code = '0'
        user_id = '1234567'
        name = 'GUESTUSER'
        password = 'pword'
        service_id = '1'

        response = Element('a_lgu')
        response.set('r', response_login_code)
        response.set('u', user_id)
        response.set('n', name)
        response.set('p', password)
        response.set('s', service_id)

        self.queue_response(response)

    def handle_a_gsd(self, request):
        # NOTE the game closes the connection when this is sent
        service_id = request.get('s')

        global host_ip
        global host_port

        bin_ip = host_ip # NOTE purpose of this is unknown
        bin_port = '0' # as above

        response = Element('a_gsd')
        response.set('s', service_id)
        response.set('xi', host_ip)
        response.set('xp', host_port)
        response.set('bi', bin_ip)
        response.set('bp', bin_port)

        self.queue_response(response)

    def handle_a_gpd(self, request):
        plugin_id = request.get('p')
        # TODO check plugin with given id exists
        global host_ip
        global host_port

        bin_ip = host_ip # NOTE purpose of this is unknown
        bin_port = '0' # must be 0 otherwise plugins won't accept responses
        service_id = plugin_id

        response = Element('a_gpd')
        response.set('s', service_id)
        response.set('p', plugin_id)
        response.set('xi', host_ip)
        response.set('xp', host_port)
        response.set('bi', bin_ip)
        response.set('bp', bin_port)

        self.queue_response(response)

    def handle_a_gsl(self, request):
        pass

    def handle_a_gfl(self, request):
        pass

    def handle_a_alo(self, request):
        pass

    def handle_p(self, request):
        # TODO use this to send the client 'waiting messages'
        time = '1'

        response = Element('p')
        response.set('t', time)

        self.queue_response(response)