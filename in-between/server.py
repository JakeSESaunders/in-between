import sys
import socketserver
from socketserver import BaseRequestHandler
from plugins.user import PluginUser
from plugins.chat import PluginChat
from plugins.galaxy import PluginGalaxy
# from plugins.fight as PluginFight
from plugins.trunk import PluginTrunk
import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element
from data.user import User, check_login
from data.userlist import UserList
import data.setup as setup

# List of user objects for the clients currently connected to the server.
user_list = UserList()

class InBetweenHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.user = None
        self.plugins = {
            1: PluginUser(1),
            2: PluginChat(2),
            7: PluginGalaxy(7),
            # 8: PluginFight(8),
            10: PluginTrunk(10)
        }
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        """Handles a TCP connection"""
        print('New Connection!')
        while True:
            raw_requests = bytearray()
            while True:
                rq = self.request.recv(128)
                if len(rq) <= 0:
                    print('Connection Closed')
                    self.request.close()
                    return
                if rq[-1] == 0x00:
                    raw_requests += rq
                    break
                raw_requests += rq
            if len(raw_requests) > 0:
                encoded_responses = self.handle_raw_requests(raw_requests)
                for encoded_response in encoded_responses:
                    self.request.send(encoded_response)

    # TODO figure out how to call this
    def finish(self):
        if self.user is not None:
            global user_list
            user_list.user_disconnect(self.user.user_id)
            print(f'[DISCONNECT]: User {self.user.user_id} left the server.')

    def handle_raw_requests(self, raw_requests):
        """Accept a bytearray of request data, return a list of appropriate bytearray responses."""
        encoded_requests = raw_requests.split(b'\x00')[:-1] # the final element should be empty
        encoded_responses = []

        for encoded_request in encoded_requests:
            print(f'[REQ {self.client_address}]: {encoded_request}')

            decoded_request = encoded_request.decode('latin-1')

            request_end_char = len(decoded_request) - decoded_request[::-1].index('>')
            xml_request = ElementTree.fromstring(decoded_request[:request_end_char])
            routing_string = decoded_request[request_end_char:]

            if len(routing_string) == 0:
                xml_response = self.handle_request(xml_request)
            else:
                ids = routing_string.split('|')
                plugin_id = int(ids[0])
                xml_response = self.handle_plugin_request(xml_request, plugin_id)

            if xml_response is not None:
                encoded_response = bytearray(ElementTree.tostring(xml_response))
                encoded_response.append(0x00)
                encoded_responses.append(encoded_response)

                print(f'[RES {self.client_address}]: {encoded_response}')

        return encoded_responses

    def handle_request(self, request):
        route = request.tag
        if route == 'a_lru':
            return self.login_registered_user(request)
        if route == 'a_lgu':
            return self.login_guest_user(request)
        if route == 'a_gsd':
            return self.get_service_details(request)
        if route == 'a_gpd':
            return self.get_plugin_details(request)
        if route == 'a_gsl':
            return self.get_service_list(request)
        if route == 'a_gfl':
            return self.get_file_list(request)
        if route == 'a_alo':
            return self.another_login(request)
        if route == 'p':
            return self.ping(request)
        raise ValueError(f'No route with id {route}.')

    def login_registered_user(self, request):
        request_login_code = request.get('l')
        name = request.get('n')
        password = request.get('p')

        service_id = '1' # NOTE arbitrary constant

        response = Element('a_lru')

        user_id = check_login(name, password)
        if user_id is not None:
            response_login_code = '0'
            response.set('u', user_id)
        
            client_address = self.client_address
            user = User(client_address, user_id)
        else:
            response_login_code = '1'
            
        response.set('r', response_login_code)
        response.set('s', service_id)

        return response

    def login_guest_user(self, request):
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

        return response

    def get_service_details(self, request):
        # NOTE the game closes the connection when this is sent
        service_id = request.get('s')

        host_ip = 'localhost'
        host_port = '80'
        bin_ip = 'localhost' # NOTE purpose of this is unknown
        bin_port = '0' # as above

        response = Element('a_gsd')
        response.set('s', service_id)
        response.set('xi', host_ip)
        response.set('xp', host_port)
        response.set('bi', bin_ip)
        response.set('bp', bin_port)

        return response

    def get_plugin_details(self, request):
        plugin_id = request.get('p')
        # TODO check plugin with given id exists
        host_ip = 'localhost'
        host_port = '80'
        bin_ip = 'localhost' # NOTE purpose of this is unknown
        bin_port = '0' # must be 0 otherwise plugins won't accept responses
        service_id = plugin_id

        response = Element('a_gpd')
        response.set('s', service_id)
        response.set('p', plugin_id)
        response.set('xi', host_ip)
        response.set('xp', host_port)
        response.set('bi', bin_ip)
        response.set('bp', bin_port)

        return response

    def get_service_list(self, request): # TODO
        response = Element('a_gsl')

        return response

    def get_file_list(self, request): # TODO
        response = Element('a_gfl')
        
        return response

    def another_login(self, request): # TODO
        response = Element('a_alo')

    def ping(self, request):
        # TODO use this to send the client 'waiting messages'
        time = '1'

        response = Element('p')
        response.set('t', time)

        return response

    def handle_plugin_request(self, request, plugin_id):
        if plugin_id in self.plugins:
            return self.plugins[plugin_id].handle_request(request)
        raise ValueError(f'No plugin with id {plugin_id}.')

    def set_user(self, user):
        self.user = user
        for plugin in self.plugins.values():
            plugin.user = user
        global user_list
        user_list.user_connect(user)

def start_server(ip, port):
    address = (ip, port)
    with socketserver.ThreadingTCPServer(address, InBetweenHandler) as server:
        print('Server started! Looking for connections...')
        server.serve_forever()

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == 'setup':
            setup.setup_database()
        else:
            start_server('localhost', 80)
    else:
        start_server('localhost', 80)
