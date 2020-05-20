from xml.etree.ElementTree import Element

isInChatSession = False

def handle_jn(xml): # Example data <jn t="3"><pr dl="0| | " f="000000CD" uid="2734650" n="TEST" /></jn>
    """Join"""
    t = xml.get('t') # room type
    pr = xml.find('pr')
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
    
def handle_lv(xml):
    """Leave"""
    id = xml.get('id')
    t = xml.get('t')

    response = Element('lv')

    global isInChatSession
    if isInChatSession: 
        isInChatSession = False
        return response
    return None

def handle_pj(xml):
    """Player List/Join"""
    pass

def handle_ms(xml):
    """Message"""
    m = xml.get('m')
    t = xml.get('t')
    id = xml.get('id')

    name = 'TEST'
    message = m

    response = Element('ms')
    response.set('n', name)
    response.set('m', message)

    return response

def handle_pd(xml):
    """Player Remove"""
    pass

def handle_of(xml):
    """Player Disconnected"""
    pass

def handle_on(xml):
    """Player Connected"""
    pass

def handle_se(xml):
    """Special Event"""
    event = xml[0]
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

def handle_cr(xml):
    """Create Room"""
    pass

def handle_cd(xml):
    """Creator Disconnect (Leave Crib)"""
    pass

def handle_cp(xml):
    """Player Properties?""" # changes the funkey
    pass

def handle_ko(xml):
    """Kick Out"""
    pass

def handle_p(xml):
    """Ping"""
    # this route sends the client info that it 'isn't asking for'

routes = {
    "jn": handle_jn,
    "lv": handle_lv,
    "pj": handle_pj,
    "ms": handle_ms,
    "pd": handle_pd,
    "of": handle_of,
    "on": handle_on,
    "se": handle_se,
    "cr": handle_cr,
    "cd": handle_cd,
    "cp": handle_cp,
    "ko": handle_ko,
    "p": handle_p
}

def handle_request(xml):
    route = xml.tag
    # may need to handle ping slightly differently
    if route in routes:
        info = routes[route](xml)
        response = Element('h2_0')
        if info is not None: # ideally this will never happen
            response.append(info)
        return response
    raise ValueError(f'No route with id {route} registered to chat.')