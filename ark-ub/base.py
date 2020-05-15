import xml.etree.ElementTree as ElementTree

def handle_a_lru(xml):
    """Login a Registered User"""
    login_code = xml.get('l')
    password = xml.get('p')
    name = xml.get('n')

    print(f'Login Registered User! Name: {name}, Password: {password}')

    login_code = 0 # NOTE this can take values from 0 to 5 but only 0 allows the player to login
    user_id = 2734650 # NOTE this is an arbitrary constant for now
    service_id = 1 # as above

    return ElementTree.fromstring(f'<a_lru r="{login_code}" u="{user_id}" s="{service_id}" />')

def handle_a_lgu(xml):
    """Login a Guest User"""
    d = xml.get('d')
    a = xml.get('a')
    c = xml.get('c')

    print(f'Login Guest User!')

    return ElementTree.fromstring(f'<a_lgu />')

def handle_a_gsd(xml):
    """Get Service Details"""
    service_id = xml.get('s')

    print(f'Get Service Details! ID: {service_id}')

    host_ip = 'localhost'
    host_port = 80
    bin_ip = 'localhost' # NOTE the purpose of this is unknown
    bin_port = 80 # as above

    return ElementTree.fromstring(f'<a_gsd xi="{host_ip}" xp="{host_port}" bi="{bin_ip}" bp="{bin_port}" s="{service_id}" />')

def handle_a_gpd(xml):
    """Get Plugin Details"""
    plugin_id = xml.get('p')

    print(f'Get Plugin Details! ID: {plugin_id}')

    host_ip = 'localhost'
    host_port = 80
    bin_ip = 'localhost' # NOTE the purpose of this is unknown
    bin_port = 80 # as above
    service_id = 1 # NOTE arbitrary constant for now
    
    return ElementTree.fromstring(f'<a_gpd xi="{host_ip}" xp="{host_port}" bi="{bin_ip}" bp="{bin_port}" s="{service_id}" p="{plugin_id}"/>')

def handle_a_gsl(xml):
    """Get Service List"""
    return ElementTree.fromstring(f'<a_gsl />')

def handle_a_gfl(xml):
    """Get File List"""
    return ElementTree.fromstring(f'<a_gfl />')

def handle_a_alo(xml):
    """Accept Another Login?"""
    return ElementTree.fromstring(f'<a_alo />')