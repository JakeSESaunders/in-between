import socketserver
import base
import plugins.user as user
import plugins.chat as chat
import plugins.galaxy as galaxy
import plugins.fight as fight
import plugins.trunk as trunk
import xml.etree.ElementTree as ElementTree

plugins = {
    0: base.handle_request,
    1: user.handle_request,
    2: chat.handle_request,
    7: galaxy.handle_request,
    8: fight.handle_request,
    10: trunk.handle_request
}

class InBetweenHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """Handles a TCP connection"""
        print('New Connection!')
        while True:
            raw_messages = bytearray()
            # Receive messages as they arrive
            while True:
                msg = self.request.recv(128)
                if len(msg) <= 0:
                    break
                if msg[-1] == 0x00:
                    raw_messages += msg
                    break
                raw_messages += msg
            if len(raw_messages) > 0:
                messages = raw_messages.split(b'\x00')
                print(f'[Requests to Handle]: {messages[:-1]}')
                for raw_request in messages[:-1]:
                    decoded_request = raw_request.decode('latin-1')
                    request_end_char = len(decoded_request) - decoded_request[::-1].index('>')

                    routing_string = decoded_request[request_end_char:]
                    xml_request = ElementTree.fromstring(decoded_request[:request_end_char])
                    
                    if len(routing_string) == 0:
                        plugin_id = 0
                    else:
                        ids = routing_string.split('|')
                        if int(ids[0]) in plugins:
                            plugin_id = int(ids[0])
                        else:
                            raise ValueError(f'Plugin with id {plugin_id} not registered.')
                    xml_response = plugins[plugin_id](xml_request)

                    if xml_response is not None:
                        raw_response = bytearray(ElementTree.tostring(xml_response))
                        raw_response.append(0x00)
                        self.request.send(raw_response)
                        print(f'[Request]: {raw_request}')
                        print(f'[Response]: {raw_response}')

if __name__ == "__main__":
    address = ('localhost', 80)
    with socketserver.ThreadingTCPServer(address, InBetweenHandler) as server:
        print('Server started! Looking for connections...')
        server.serve_forever()
