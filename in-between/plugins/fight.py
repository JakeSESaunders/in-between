from xml.etree.ElementTree import Element

def handle_jn(xml):
    pr, c = xml.get('pr'), xml.get('c') # c is challenge, 0 for random, 1 for buddy

    r = '1'
    bid = '0'
    p = '10'

    response = Element('jn')
    response.set('r', r)
    response.set('bid', bid)
    response.set('p', p)
    
    return response

def handle_lv(xml):
    bid = xml.get('bid')

    response = Element('lv')

    return response

def handle_p(xml):
    pass

routes = {
    "jn": handle_jn,
    "lv": handle_lv
}

def handle_request(xml):
    route = xml.tag
    if route in routes:
        response = Element('h8_0')
        info = routes[route](xml)
        if info is not None:
            response.append(info)
        return response
    raise ValueError(f'No route with id {route} registered to fight.')