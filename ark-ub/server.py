import socket
import base
import xml.etree.ElementTree as ElementTree

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 80))
serversocket.listen(5)

request_handlers = {
    "a_lru": base.handle_a_lru,
    "a_lgu": base.handle_a_lgu,
    "a_gsd": base.handle_a_gsd,
    "a_gpd": base.handle_a_gpd,
    "a_gsl": base.handle_a_gsl,
    "a_gfl": base.handle_a_gfl,
    "a_alo": base.handle_a_alo
}

def handle_request(xml):
    """Handles xml request, sends appropriate xml response. Translation to/from bytes is NOT done here."""
    route = xml.tag
    if route in request_handlers:
        return request_handlers[route](xml)
    raise ValueError(f'No registered request handler for route {route}')

while True:
    # accept connections from outside
    print("Looking for connections...")
    (clientsocket, address) = serversocket.accept()
    print("Found connection!", address)
    raw_messages = bytearray()
    while True:
        msg = clientsocket.recv(128)
        if len(msg) <= 0:
            break
        if msg[-1] == 0x00:
            raw_messages += msg
            break
        raw_messages += msg
    # split message into individual messages
    messages = raw_messages.split(b'\x00')
    print(f'[Requests to Handle]: {messages[:-1]}')
    for raw_request in messages[:-1]:
        # decode to xml, find response, encode to bytes, send response
        decoded_request = raw_request.decode('latin-1')
        xml_request = ElementTree.fromstring(decoded_request)
        xml_response = handle_request(xml_request)
        raw_response = bytearray(ElementTree.tostring(xml_response))
        raw_response.append(0x00)
        clientsocket.send(raw_response)
        print(f'[Request]: {raw_request}')
        print(f'[Response]: {raw_response}')
    clientsocket.close()
