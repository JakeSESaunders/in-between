import sys
import socketserver
from socketserver import BaseRequestHandler
from plugins.base import PluginBase
from plugins.user import PluginUser
from plugins.chat import PluginChat
from plugins.galaxy import PluginGalaxy
from plugins.trunk import PluginTrunk
from plugins.webservice import handle_http
import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element
import data.setup as setup
from data.volatile import userlist
from data.user.user import User, login
from settings import host_internal_ip, host_ip, host_port, debug, blocked_addresses
from data.volatile import chatrooms

# TODO implement logging to text file

class InBetweenHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.user = None
        self.plugins = {
            1: PluginUser(1),
            2: PluginChat(2),
            7: PluginGalaxy(7),
            10: PluginTrunk(10)
        }
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        """Handles a TCP connection."""
        print(f'[CONNECT]: New connection from {self.client_address}')

        global blocked_addresse
        if self.client_address[0] in blocked_addresses:
            print(f'[DISCONNECT]: Address {self.client_address[0]} blocked from server')
            self.request.close()
            return
            
        while True:
            raw_requests = bytearray()
            while True:
                try:
                    rq = self.request.recv(128)
                except:
                    print(f'[ERROR]: Connection to {self.client_address} closed unexpectedly')
                    self.request.close()
                    # TODO close connection cleanly, remove from chats and multiplayer games etc
                    global chatrooms
                    if self.user is not None:
                        chatrooms.disconnect(self.user.user_id)
                    return
                if len(rq) <= 0:
                    self.request.close() # TODO meant to have some kind of shutdown thing here?
                    return
                if rq[-1] == 0x00:
                    raw_requests += rq
                    break
                raw_requests += rq
                if '\r\n\r\n' in raw_requests.decode('iso-8859-1'):
                    break
            if '\r\n\r\n' in raw_requests.decode('iso-8859-1'):
                self.handle_raw_http(raw_requests)
            elif len(raw_requests) > 0:
                self.handle_raw_requests(raw_requests)
            self.send_responses()

    # TODO figure out how to call this
    def finish(self):
        """Called when TCP connection closed."""
        print(f'[DISCONNECT]: User at {self.client_address} disconnected')
        global userlist
        if self.user is not None:
            userlist.disconnect(self.user.user_id)

    def send_response(self, response):
        """Send an XML response to the client."""
        encoded_response = bytearray(ElementTree.tostring(response))
        encoded_response.append(0x00)
        self.request.send(encoded_response)

        global debug
        if debug:
            print(f'[RES {self.client_address}]: {encoded_response.decode("latin-1")}')

    def send_responses(self):
        """Send all queued responses."""
        responses = []
        for plugin in self.plugins.values():
            responses += plugin.get_responses()
        for response in responses:
            self.send_response(response)
        
    def handle_raw_requests(self, raw_requests):
        """Accept a bytearray of request data, send the data to the appropriate handlers."""
        encoded_requests = raw_requests.split(b'\x00')[:-1] # the final element should be empty

        for encoded_request in encoded_requests:
            decoded_request = encoded_request.decode('latin-1')
            global debug
            if debug:
                print(f'[REQ {self.client_address}]: {decoded_request}')

            request_end_char = len(decoded_request) - decoded_request[::-1].index('>')
            xml_request = ElementTree.fromstring(decoded_request[:request_end_char])
            routing_string = decoded_request[request_end_char:]

            plugin_id = -1
            if len(routing_string) == 0:
                self.handle_base_request(xml_request)
            else:
                ids = routing_string.split('|')
                plugin_id = int(ids[0])
                self.handle_request(xml_request, plugin_id)

    def handle_raw_http(self, request):
        # TODO this needs improvement to check for malicious requests, but it'll do for now

        # Parse the head
        partial_request_string = request.decode('iso-8859-1')
        head_end_index = partial_request_string.find('\r\n\r\n')
        body_start_index = head_end_index + 4 # to account for \r\n\r\n
        head_string = partial_request_string[:head_end_index]
        head_parts = head_string.split('\r\n')

        start_line_parts = head_parts[0].split(' ')
        method, path, version = start_line_parts[0], start_line_parts[1], start_line_parts[2]

        headers = {}
        for header_data in head_parts[1:]:
            if ': ' in header_data:
                header_data_split = header_data.split(': ')
                headers[header_data_split[0]] = header_data_split[1]

        encoded_request = request

        # Get the entire remaining message (if any body exists)
        if 'Content-Length' in headers.keys():
            content_length = int(headers['Content-Length'])
            remaining_content_length = content_length - len(partial_request_string[body_start_index:].encode('iso-8859-1'))
            print(f'Content-Length: {remaining_content_length}')
            # TODO respond 413 if content-length is too large
            if remaining_content_length > 0:
                request_end = self.request.recv(remaining_content_length)
                encoded_request = request + request_end
            
        decoded_request = encoded_request.decode()
        body = decoded_request[body_start_index:]

        print(f'[WEB REQ {self.client_address}]: {decoded_request}')

        # Send to webservice plugin
        decoded_response = handle_http(method, path, version, headers, body)
        if decoded_response is not None:
            print(f'[WEB RES {self.client_address}]: {decoded_response}')

            # Send response to client
            encoded_response = decoded_response.encode('iso-8859-1')
            self.request.send(encoded_response)

    def handle_request(self, request, plugin_id):
        if plugin_id in self.plugins:
            self.plugins[plugin_id].handle_request(request)
        else:
            raise ValueError(f'No plugin with id {plugin_id}.')

    # these requests don't queue a response, they send it directly
    def handle_base_request(self, request):
        route = request.tag
        if route == 'a_lru':
            self.handle_a_lru(request)
            return
        if route == 'a_lgu':
            self.handle_a_lgu(request)
            return
        if route == 'a_gsd':
            self.handle_a_gsd(request)
            return
        if route == 'a_gpd':
            self.handle_a_gpd(request)
            return
        if route == 'a_gsl':
            self.handle_a_gsl(request)
            return
        if route == 'a_gfl':
            self.handle_a_gfl(request)
            return
        if route == 'a_alo':
            self.handle_a_alo(request)
            return
        if route == 'p':
            self.handle_p(request)
            return

    # TODO somehow implement these requests in a more elegant way
    def handle_a_lru(self, request):
        request_login_code = request.get('l')
        name = request.get('n')
        password = request.get('p')

        response = Element('a_lru')

        global userlist

        user_id = login(name, password)
        if user_id is not None:
            response_login_code = userlist.connect(user_id, self)
            self.user = User(user_id, self)
        else:
            response_login_code = 1

        service_id = '1' # NOTE arbitrary constant

        response.set('r', str(response_login_code))
        response.set('u', str(user_id))
        response.set('s', str(service_id))

        self.send_response(response)

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

        self.send_response(response)

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
        response.set('xp', str(host_port))
        response.set('bi', bin_ip)
        response.set('bp', bin_port)

        self.send_response(response)

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
        response.set('xp', str(host_port))
        response.set('bi', bin_ip)
        response.set('bp', bin_port)

        self.send_response(response)

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

        self.send_response(response)

def start_server():
    global host_ip
    global host_port
    address = (host_internal_ip, host_port)
    with socketserver.ThreadingTCPServer(address, InBetweenHandler) as server:
        print(f'Server started at {host_ip}:{host_port}! Looking for connections...')
        server.serve_forever()

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == 'setup':
            setup.setup_database()
        else:
            start_server()
    else:
        start_server()
