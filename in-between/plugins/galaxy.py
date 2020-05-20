from xml.etree.ElementTree import Element

def handle_lpv(xml):
    # no params to get
    version = '0'

    response = Element('lpv')
    response.set('v', version)

    return response

def handle_vsu(xml):
    response = Element('vsu')

    return response

def handle_sp(xml):
    """Save Profile"""
    response = Element('sp')

    return response

def handle_rr(xml):
    response = Element('rr')

    return response

def handle_profile(xml):
    response = Element('profile')

    return response

def handle_ge(xml):
    response = Element('ge')

    return response

def handle_gls(xml):
    """Get Leaderboard Statistics"""
    stat_type = xml.get('id') # 1 for games, 2 for items

    response = Element('gls')
    response.set('id', stat_type)

    game_records = [
        {
            'game_id': '6',
            'sp': '500',
            'mp': '600'
        },
        {
            'game_id': '7',
            'sp': '700',
            'mp': '800'
        }
    ]

    item_records = [
        {
            'item_id': '1a',
            'count': '55'
        }
    ]

    records = Element('records')
    records.set('id', stat_type)

    if stat_type == '1':
        for record_data in game_records:
            record = Element('record')
            record.set('id', record_data['game_id'])
            record.set('sp', record_data['sp'])
            record.set('mp', record_data['mp'])

            records.append(record)
    elif stat_type == '2':
        for record_data in item_records:
            record = Element('record')
            record.set('id', record_data['item_id'])
            record.set('c', record_data['count'])

            records.append(record)
            
    response.append(records)

    return response

def handle_p(xml):
    pass

routes = {
    "lpv": handle_lpv,
    "vsu": handle_vsu,
    "sp": handle_sp,
    "rr": handle_rr,
    "profile": handle_profile,
    "ge": handle_ge,
    "gls": handle_gls,
    "p": handle_p
}

def handle_request(xml):
    route = xml.tag
    if route in routes:
        response = Element('h7_0')
        info = routes[route](xml)
        if info is not None:
            response.append(info)
        return response
    raise ValueError(f'No route with id {route} registered to base.')