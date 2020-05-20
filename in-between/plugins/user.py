from xml.etree.ElementTree import Element

def handle_u_gcl(xml):
    """Get Currency List"""
    pass

def handle_u_gwl(xml):
    """Get Country List"""
    pass

def handle_u_gul(xml):
    """Get USA States List"""
    pass

def handle_u_gfl(xml):
    """Get File List"""
    pass

def handle_u_reg(xml):
    """Register"""
    login = xml.get('l')
    password = xml.get('p')
    client_id = xml.get('c')
    affiliate_id = xml.get('a')
    ad_id = xml.get('d')
    secret_answer = xml.get('sa')
    secret_question = xml.get('sq')

    r = '0' # can take values 0-5, 90 and 99
    user_id = '2734650'

    response = Element('u_reg')
    response.set('r', r)
    response.set('u', user_id)

    return response

def handle_u_sup(xml):
    """Send Update Profile"""
    pass

def handle_u_gup(xml):
    """Get User Profile"""
    pass

def handle_u_gsp(xml):
    """Get Short Profile"""
    pass

def handle_u_gus(xml):
    """Get User Stats"""
    pass

def handle_u_spm(xml):
    """Send Private Message"""
    r = '0' # can take values 0-3 and 99, only 0-2 do anything
    f = xml.get('f') # from id
    t = xml.get('t') # to id
    m = xml.get('m') # message

    response = Element('u_spm')
    response.set('r', r)
    response.set('f', f)
    response.set('t', t)
    response.set('m', m)

    return response

def handle_u_gsq(xml):
    """Get Secure Question?"""
    pass

def handle_u_acp(xml):
    """Account Change Password"""
    pass

def handle_u_afp(xml):
    """Account Forgot Password"""
    pass

def handle_u_rpm(xml):
    """Receive Private Message"""
    pass

def handle_u_gbl(xml):
    """Get Buddy List"""
    r = '0' # can take values 0 or 1
    # for each buddy, add a child node with the following:

    response = Element('u_gbl')
    response.set('r', r)

    buddy_list = [
        {
            'id': '512',
            'name': 'GREG',
            'online': '1',
            'status': '0',
            'bf': '0',
            'cf': '0',
            'ph': '1'
        },
        {
            'id': '513',
            'name': 'NOTGREG',
            'online': '1',
            'status': '0',
            'bf': '0',
            'cf': '0',
            'ph': '1'
        }
    ]

    for buddy in buddy_list:
        buddy_data = Element('bd')
        buddy_data.set('id', buddy['id'])
        buddy_data.set('n', buddy['name'])
        buddy_data.set('o', buddy['online'])
        buddy_data.set('s', buddy['status'])
        buddy_data.set('bf', buddy['bf'])
        buddy_data.set('cf', buddy['cf'])
        buddy_data.set('ph', buddy['ph'])

        response.append(buddy_data)

    return response

def handle_u_abd(xml):
    """Add Buddy"""
    buddy_name = xml.get('n')

    r = '0' # can take values 0-3
    n = 'SOMEONE' # name
    a = '1'
    b = '512' # id
    o = '0' # online
    s = '0' # status
    bf = '0'
    cf = '0'
    ph = '0'

    response = Element('u_abd')
    response.set('r', r)
    response.set('n', n)
    response.set('a', a)
    response.set('b', b)
    response.set('o', o)
    response.set('s', s)
    response.set('bf', bf)
    response.set('cf', cf)
    response.set('ph', ph)

    return response

def handle_u_abr(xml):
    """Add Buddy Request"""
    b = '512' # id
    n = 'SOMEONEELSE' # name

    response = Element('u_abr')
    response.set('b', b)
    response.set('n', n)

    return response
    
def handle_u_dbd(xml):
    """Delete Buddy"""
    pass

def handle_u_dbr(xml):
    """Delete Buddy Request"""
    pass

def handle_u_fbd(xml):
    """Flag? Buddy"""
    pass

def handle_u_ccs(xml):
    """Chat Status (Buddy's chat status?)"""
    new_status = xml.get('s') # can take values 0 for ready to party or 1 for dnd
    user_id = '2734650'

    response = Element('u_ccs')
    response.set('id', user_id)
    response.set('s', new_status)

    return response   

def handle_u_cph(xml):
    """Change Phone Status"""
    ph_in = xml.get('ph')

    user_id = '2734650'
    ph_out = ph_in

    response = Element('u_cph')
    response.set('u', user_id)
    response.set('ph', ph_out)

    return response

def handle_u_cos(xml):
    """Change Online Status"""
    pass

def handle_u_gcb(xml):
    """Get Coin Balance"""
    pass

# Appears to not be implemented
def handle_u_gth(xml):
    """Get Transaction History"""
    pass

def handle_u_inv(xml):
    """Invitation"""
    pass

def handle_u_inr(xml):
    """Invitaation Response"""
    pass

def handle_u_p(xml):
    """Ping"""
    t = '1'

    response = Element('u_p')
    response.set('t', t)
    
    return response

def handle_p(xml):
    """Ping"""
    t = '1'

    response = Element('p')
    response.set('t', t)
    
    return response

routes = {
    "u_gcl": handle_u_gcl,
    "u_gwl": handle_u_gwl,
    "u_gul": handle_u_gul,
    "u_gfl": handle_u_gfl,
    "u_reg": handle_u_reg,
    "u_sup": handle_u_sup,
    "u_gup": handle_u_gup,
    "u_gsp": handle_u_gsp,
    "u_gus": handle_u_gus,
    "u_spm": handle_u_spm,
    "u_gsq": handle_u_gsq,
    "u_acp": handle_u_acp,
    "u_afp": handle_u_afp,
    "u_rpm": handle_u_rpm,
    "u_gbl": handle_u_gbl,
    "u_abd": handle_u_abd,
    "u_abr": handle_u_abr,
    "u_dbd": handle_u_dbd,
    "u_dbr": handle_u_dbr,
    "u_fbd": handle_u_fbd,
    "u_ccs": handle_u_ccs,
    "u_cph": handle_u_cph,
    "u_cos": handle_u_cos,
    "u_gcb": handle_u_gcb,
    "u_gth": handle_u_gth,
    "u_inv": handle_u_inv,
    "u_inr": handle_u_inr,
    "u_p": handle_u_p,
    "p": handle_p
}

def handle_request(xml):
    route = xml.tag
    if route in routes:
        response = routes[route](xml)
        if response is not None:
            return routes[route](xml)
        else:
            raise ValueError(f'No response for route {route}.')
    raise ValueError(f'No route with id {route} registered to user.')