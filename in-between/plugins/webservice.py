import xml.etree.ElementTree as ElementTree

bad_request = {
    'start-line': 'HTTP/1.1 400 Bad Request',
    'headers': {},
    'body': None
}

not_found = {
    'start-line': 'HTTP/1.1 404 Not Found',
    'headers': {},
    'body': None
}

def handle_http(method, path, version, headers, body):
    if method == 'GET':
        response = handle_get(path, headers)
    elif method == 'POST':
        response = handle_post(path, headers, body)
    else:
        global bad_request
        response = bad_request
        raise ValueError(f'No route registered for method {method}.')
    if response is not None:
        response_string = build_response(response)
        return response_string

def handle_get(path, headers):
    if path == '/FilestoreV2/Store.xml':
        pass
    else:
        global not_found
        response = not_found

def handle_post(path, headers, body):
    if path == '/':
        # This means we have a netcommand to handle
        netcommand = ElementTree.fromstring(body)
        response = handle_netcommand(netcommand)
    else:
        global not_found
        response = not_found
    return response

def handle_netcommand(netcommand):
    installation_id = netcommand.get('installationid')
    user_id = netcommand.get('userid')
    name = netcommand.get('name')
    password = netcommand.get('pass')
    h = netcommand.get('h')
    confirm = netcommand.get('confirm')

    command_xml = netcommand[0]
    command = command_xml.tag

    global bad_request

    if command == 'loadcrib':
        response = handle_loadcrib(command_xml)
    elif command == 'savecrib':
        response = bad_request
    else:
        response = bad_request
    return response

def build_response(response):
    start_line, headers, body = response['start-line'], response['headers'], response['body']
    response_string = ''
    response_string += start_line
    response_string += '\r\n'
    for header in headers.keys():
        response_string += f'{header}: {headers[header]}\r\n'
    response_string += '\r\n'
    if body is not None:
        response_string += body
    return response_string

def handle_loadcrib(netcommand):
    start_line = 'HTTP/1.1 200 OK'
    headers = {
        'Server': 'InBetween/0.1',
        'Content-Type': 'text/html',
        'Content-Length': '3847'
    }
    # Cannot have any newlines or unnecessary whitespace here or the game hangs
    body = '''<loadcrib result="0" reason="Something?" currCrib="1" name="TEST2"><profile crib_name="TEST" name="LAKO" car="1"><zones><zone id="city"><gem count="0"><shard has_shard="0" score="1775" game="6" /><shard has_shard="0" score="1069551" game="40" /><shard has_shard="0" score="216400" game="4" /><shard has_shard="0" score="3120" game="3" /><shard has_shard="0" score="0" game="9" /><shard has_shard="0" score="0" game="39" /></gem><map tiles="1001111111111111111101111" /><removed-objects /></zone><zone id="lava"><gem count="0"><shard has_shard="0" score="8135" game="2" /></gem><map tiles="0011100111111111111101001" /><removed-objects><object kind="fossilcollector" type="distraction" id="Fossil_part_1" /></removed-objects></zone><zone id="space"><gem count="0"><shard has_shard="0" score="187550" game="10" /><shard has_shard="1" score="105150" game="5" /></gem><map tiles="0111101111111111111100110" /><removed-objects /></zone><zone id="underwater"><gem count="0" /><map tiles="0000000000000000000000000" /><removed-objects /></zone><zone id="island"><gem count="0" /><map tiles="0000001000010000100001100" /><removed-objects /><bridges is_open="0" /></zone><zone id="night"><gem count="0"><shard has_shard="0" score="23" game="30" /></gem><map tiles="0000100001000110001100000" /><removed-objects /></zone><zone id="day"><gem count="0" /><map tiles="0000000000000000000000000" /><removed-objects /></zone><zone id="green"><gem count="0" /><map tiles="0001001111010110111111011" /><removed-objects /></zone><zone id=""><gem count="0"><shard has_shard="0" score="0" game="49" /></gem><map tiles="0000000000000000000000000" /><removed-objects /></zone><zone id="realm"><gem count="0" /><map tiles="0000000000000000000001000" /><removed-objects /></zone></zones><games><game zone="city" is_free="true" id="4" /><game zone="space" is_free="true" id="10" /><game zone="space" is_free="true" id="5" /><game cnt="1" zone="green" is_free="false" id="49" /></games><chats /><trophies><trophy gameid="2" points="8135" id="1" /><trophy gameid="10" points="91650" id="9" /><trophy gameid="5" points="105150" id="4" /></trophies><milestones><milestone id="1" /><milestone id="3" /><milestone id="58" /><milestone id="20" /><milestone id="23" /><milestone id="17" /><milestone id="19" /><milestone id="38" /><milestone id="53" /><milestone id="45" /><milestone id="37" /><milestone id="34" /><milestone id="2" /><milestone zone="city" id="22" /><milestone id="36" /><milestone id="25" /><milestone id="59" /><milestone zone="space" id="5" /><milestone id="10" /><milestone id="46" /><milestone id="60" /></milestones><bitty-crib><screens><screen rid="l" id="0" name="Living Room"><layout id="5"><walls><wall id="0" fill="2g" /><wall id="1" fill="2g" /><wall id="2" fill="2g" /><wall id="3" fill="2g" /><wall id="4" fill="2g" /><wall id="5" fill="2g" /></walls><floor type="0" fill="0xc9c9c9" id="2" /><floor type="0" fill="2g" id="1" /><floor type="0" fill="0x015aff" id="0" /><trim fill="" /></layout><items><item scale="100" y="413" x="350" id="6c" /><item scale="100" y="450" x="475" id="8c" /><item scale="100" y="425" x="325" id="10f" /><item depths="300" scale="100" y="432" x="370" id="18g" /><item scale="100" y="475" x="525" id="40e" /><item scale="100" y="225" x="325" id="70123e" /><item scale="100" y="238" x="400" id="70123b" /><item scale="100" y="313" x="350" id="70123f" /><item scale="100" y="375" x="525" id="70123c" /><item scale="100" y="325" x="475" id="70123a" /><item scale="100" y="175" x="225" id="361e" /><item scale="100" y="413" x="600" id="422d" /></items></screen><screen rid="m" id="1" name="Game Room" /><screen rid="t" id="2" name="Trophy Room" /><screen name="Garage" rid="g" id="3"><layout id="2"><floor type="0" fill="" id="0" /><walls><wall id="0" fill="" /><wall id="1" fill="" /></walls><trim fill="" /></layout><items><item scale="100" y="310" x="603" id="390d" /><item scale="100" y="272" x="478" id="386d" /><item scale="100" y="197" x="428" id="391d" /><item scale="100" y="322" x="678" id="388e" /><item scale="100" y="460" x="653" id="384e" /><item scale="100" y="435" x="503" id="389e" /><item scale="100" y="422" x="378" id="385c" /><item scale="100" y="272" x="328" id="387a" /><item scale="100" y="372" x="228" id="383g" /><item scale="100" y="335" x="103" id="382f" /></items></screen></screens></bitty-crib><artefacts /></profile></loadcrib>'''

    response = {
        'start-line': start_line,
        'headers': headers,
        'body': body
    }

    return response