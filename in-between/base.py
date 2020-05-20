from xml.etree.ElementTree import Element

def handle_a_lru(xml):
    """Login a Registered User"""
    login_code = xml.get('l')
    password = xml.get('p')
    name = xml.get('n')

    login_code = '0' # NOTE this can take values from 0 to 5 but only 0 allows the player to login
    user_id = '2734650' # NOTE this will vary based on the player logging in
    service_id = '1' # as above

    response = Element('a_lru')
    response.set('r', login_code) # 0 for success, 1 if session already in use, 2 for general errors
    response.set('u', user_id)
    response.set('s', service_id)

    return response

def handle_a_lgu(xml): # game doesn't like when inaccurate info returned
    """Login a Guest User"""
    ad_id = xml.get('d')
    affiliate_id = xml.get('a')
    client_id = xml.get('c')

    r = '0' # can take values 0-5, 0 for success, 1 if session in use, 2 if user already connected, 3 if user can't be logged, 4 for incorrect pword, 5 for username not registered
    user_id = '2734650'
    name = 'test'
    password = 'pass'
    service_id = '1'

    response = Element('a_lgu')
    response.set('r', r)
    response.set('u', user_id)
    response.set('n', name)
    response.set('p', password)
    response.set('s', service_id)

    return response

def handle_a_gsd(xml): # game doesn't like this
    """Get Service Details"""
    service_id = xml.get('s')

    host_ip = 'localhost'
    host_port = '80'
    bin_ip = 'localhost' # NOTE the purpose of this is unknown
    bin_port = '0' # as above

    response = Element('a_gsd')
    response.set('xi', host_ip)
    response.set('xp', host_port)
    response.set('bi', bin_ip)
    response.set('bp', bin_port)
    response.set('s', service_id)

    return response

# If the client receives a malformed response for plugin #7 then it closes the connection
def handle_a_gpd(xml):
    """Get Plugin Details"""
    plugin_id = xml.get('p')

    host_ip = 'localhost'
    host_port = '80'
    bin_ip = 'localhost' # NOTE the purpose of this is unknown
    bin_port = '0' # this should be 0 otherwise plugins won't accept responses
    service_id = plugin_id

    response = Element('a_gpd')
    response.set('xi', host_ip)
    response.set('xp', host_port)
    response.set('bi', bin_ip)
    response.set('bp', bin_port)
    response.set('s', service_id)
    response.set('p', plugin_id)

    return response

def handle_a_gsl(xml):
    """Get Service List"""
    response = Element('a_gsl')
    
    return response

def handle_a_gfl(xml):
    """Get File List"""
    response = Element('a_gfl')
    
    return response

def handle_a_alo(xml):
    """Accept Another Login?"""
    response = Element('a_alo')
    
    return response

def handle_p(xml):
    """Ping"""
    time = '1'

    response = Element('p')
    response.set('t', time)

    return response

routes = {
    "a_lru": handle_a_lru,
    "a_lgu": handle_a_lgu,
    "a_gsd": handle_a_gsd,
    "a_gpd": handle_a_gpd,
    "a_gsl": handle_a_gsl,
    "a_gfl": handle_a_gfl,
    "a_alo": handle_a_alo,
    "p": handle_p
}

def handle_request(xml):
    route = xml.tag
    if route in routes:
        return routes[route](xml)
    raise ValueError(f'No route with id {route} registered to base.')