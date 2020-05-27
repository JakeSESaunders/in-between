import sys
import socketserver
from socketserver import BaseRequestHandler
from plugins.base import PluginBase
from plugins.user import PluginUser
from plugins.chat import PluginChat
from plugins.galaxy import PluginGalaxy
from plugins.trunk import PluginTrunk
import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element
from data.user import User, check_login
from data.userlist import UserList
import data.setup as setup

debug = True
# TODO implement logging

class InBetweenHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.user = None
        self.plugins = {
            0: PluginBase(0),
            1: PluginUser(1),
            2: PluginChat(2),
            7: PluginGalaxy(7),
            10: PluginTrunk(10)
        }
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        """Handles a TCP connection."""
        print(f'[CONNECT]: New connection from {self.client_address}')
        while True:
            raw_requests = bytearray()
            while True:
                try:
                    rq = self.request.recv(128)
                except:
                    print(f'[ERROR]: Connection to {self.client_address} closed unexpectedly')
                    self.request.close()
                    return
                if len(rq) <= 0:
                    self.request.close() # TODO meant to have some kind of shutdown thing here?
                    return
                if rq[-1] == 0x00:
                    raw_requests += rq
                    break
                raw_requests += rq
            if len(raw_requests) > 0:
                self.handle_raw_requests(raw_requests)
            self.send_responses()

    # TODO figure out how to call this
    def finish(self):
        """Called when TCP connection closed."""
        print(f'[DISCONNECT]: User at {self.client_address} disconnected')

    def send_response(self, response):
        """Send an XML response to the client."""
        encoded_response = bytearray(ElementTree.tostring(response))
        encoded_response.append(0x00)
        self.request.send(encoded_response)

        global debug
        if debug:
            print(f'[RES {self.client_address}]: {encoded_response}')

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
            global debug
            if debug:
                print(f'[REQ {self.client_address}]: {encoded_request}')

            decoded_request = encoded_request.decode('latin-1')

            request_end_char = len(decoded_request) - decoded_request[::-1].index('>')
            xml_request = ElementTree.fromstring(decoded_request[:request_end_char])
            routing_string = decoded_request[request_end_char:]

            plugin_id = -1
            if len(routing_string) == 0:
                plugin_id = 0
            else:
                ids = routing_string.split('|')
                plugin_id = int(ids[0])
            self.handle_request(xml_request, plugin_id)

    def handle_request(self, request, plugin_id):
        if plugin_id in self.plugins:
            self.plugins[plugin_id].handle_request(request)
        else:
            raise ValueError(f'No plugin with id {plugin_id}.')

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
