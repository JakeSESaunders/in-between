from xml.etree.ElementTree import Element

def handle_gil(xml):
    """Get Items List"""
    response = Element('gil')

    return response

def handle_gcl(xml):
    """Get Cleanings? List"""
    url = 'localhost'

    response = Element('gcl')
    response.set('url', url)
    
    return response

def handle_grl(xml):
    """Get Rooms List"""
    response = Element('grl')

    return response

def handle_gfl(xml):
    """Get Familiars List"""
    url = 'localhost'

    response = Element('gfl')
    response.set('url', url)
    
    return response

def handle_gjl(xml):
    """Get Jammers List"""
    url = 'localhost'

    response = Element('gjl')
    response.set('url', url)

    jammer_list = [
        {
            'id': '1',
            'rid': '80014a',
            'c': '5',
            'q': '6',
            'd': '0'
        },
        {
            'id': '2',
            'rid': '80014a',
            'c': '39',
            'q': '10',
            'd': '1'
        }
    ]

    for jammer_data in jammer_list:
        jammer = Element('j')
        jammer.set('id', jammer_data['id'])
        jammer.set('rid', jammer_data['rid'])
        jammer.set('c', jammer_data['c'])
        jammer.set('q', jammer_data['q'])
        jammer.set('d', jammer_data['d'])
        response.append(jammer)

    return response

def handle_gml(xml):
    """Get Moods List"""
    url = 'localhost'

    response = Element('gml')
    response.set('url', url)

    return response

def handle_glb(xml):
    """Get Loot Balance"""
    loot_balance = '10000'

    response = Element('glb')
    response.set('b', loot_balance)

    return response

def handle_gut(xml):
    """Get User Transactions"""
    response = Element('gut')

    return response

def handle_gutc(xml):
    """Get User Transactions Count"""
    transaction_count = '1'

    response = Element('gutc')
    response.set('c', transaction_count)

    return response

def handle_gsl(xml):
    """Get Splash List"""
    response = Element('gsl')

    return response

def handle_te(xml):
    """Transaction Error"""
    response = Element('te')

    return response

def handle_bi(xml):
    """Buy Item"""
    response = Element('bi')

    return response

def handle_bc(xml):
    """Buy Cleaning?"""
    response = Element('bc')

    return response

def handle_br(xml):
    """Buy Room"""
    response = Element('br')

    return response

def handle_bf(xml):
    """Buy Familiar"""
    response = Element('bf')

    return response

def handle_bm(xml):
    """Buy Mood"""
    response = Element('bm')

    return response

def handle_bj(xml):
    """Buy Jammer"""
    database_id = xml.get('id')
    new_balance = '75000'

    response = Element('bj')
    response.set('id', database_id)
    response.set('b', new_balance)
    
    return response

def handle_gua(xml):
    """Get User Asset"""
    response = Element('gua')

    return response

def handle_asp(xml):
    """Asset Parameters"""
    # for when a trunk jammer/familiar is used

    response = Element('asp')

    return response

def handle_p(xml):
    """Ping"""
    response = Element('p')

    return response

routes = {
    "gil": handle_gil,
    "gcl": handle_gcl,
    "grl": handle_grl,
    "gfl": handle_gfl,
    "gjl": handle_gjl,
    "gml": handle_gml,
    "glb": handle_glb,
    "gut": handle_gut,
    "gutc": handle_gutc,
    "gsl": handle_gsl,
    "te": handle_te,
    "bi": handle_bi,
    "bc": handle_bc,
    "br": handle_br,
    "bf": handle_bf,
    "bm": handle_bm,
    "bj": handle_bj,
    "gua": handle_gua,
    "p": handle_p
}

def handle_request(xml):
    route = xml.tag
    if route in routes:
        response = Element('h10_0')
        info = routes[route](xml)
        if info is not None:
            response.append(info)
        return response
    raise ValueError(f'No route with id {route} registered to trunk.')