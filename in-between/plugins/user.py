from plugins.plugin import Plugin
from xml.etree.ElementTree import Element

class PluginUser(Plugin):
    def __init__(self, plugin_id):
        Plugin.__init__(self, plugin_id)
        # TODO make this look a bit nicer?
        self.register_route('u_gcl', self.handle_u_gcl)
        self.register_route('u_gwl', self.handle_u_gwl)
        self.register_route('u_gul', self.handle_u_gul)
        self.register_route('u_gfl', self.handle_u_gfl)
        self.register_route('u_reg', self.handle_u_reg)
        self.register_route('u_sup', self.handle_u_sup)
        self.register_route('u_gup', self.handle_u_gup)
        self.register_route('u_gsp', self.handle_u_gsp)
        self.register_route('u_gus', self.handle_u_gus)
        self.register_route('u_spm', self.handle_u_spm)
        self.register_route('u_gsq', self.handle_u_gsq)
        self.register_route('u_acp', self.handle_u_acp)
        self.register_route('u_afp', self.handle_u_afp)
        self.register_route('u_rpm', self.handle_u_rpm)
        self.register_route('u_gbl', self.handle_u_gbl)
        self.register_route('u_abd', self.handle_u_abd)
        self.register_route('u_abr', self.handle_u_abr)
        self.register_route('u_dbd', self.handle_u_dbd)
        self.register_route('u_dbr', self.handle_u_dbr)
        self.register_route('u_fbd', self.handle_u_fbd)
        self.register_route('u_ccs', self.handle_u_ccs)
        self.register_route('u_cph', self.handle_u_cph)
        self.register_route('u_cos', self.handle_u_cos)
        self.register_route('u_gcb', self.handle_u_gcb)
        self.register_route('u_gth', self.handle_u_gth)
        self.register_route('u_inv', self.handle_u_inv)
        self.register_route('u_inr', self.handle_u_inr)
        self.register_route('u_p', self.handle_u_p)
        self.register_route('p', self.handle_p)

    def handle_request(self, request):
        """Handle an xml request directed at the plugin and return an appropriate xml response."""
        route_id = request.tag
        route_handler = self.get_route(route_id)
        response = route_handler(request)

        return response

    def handle_u_gcl(self, request):
        """Get Currency List"""
        pass

    def handle_u_gwl(self, request):
        """Get Country List"""
        pass

    def handle_u_gul(self, request):
        """Get USA States List"""
        pass

    def handle_u_gfl(self, request):
        """Get File List"""
        pass

    def handle_u_reg(self, request):
        """Register"""
        login = request.get('l')
        password = request.get('p')
        client_id = request.get('c')
        affiliate_id = request.get('a')
        ad_id = request.get('d')
        secret_answer = request.get('sa')
        secret_question = request.get('sq')

        r = '0' # can take values 0-5, 90 and 99
        user_id = '2734650'

        response = Element('u_reg')
        response.set('r', r)
        response.set('u', user_id)

        return response

    def handle_u_sup(self, request):
        """Send Update Profile"""
        pass

    def handle_u_gup(self, request):
        """Get User Profile"""
        pass

    def handle_u_gsp(self, request):
        """Get Short Profile"""
        pass

    def handle_u_gus(self, request):
        """Get User Stats"""
        pass

    def handle_u_spm(self, request):
        """Send Private Message"""
        r = '0' # can take values 0-3 and 99, only 0-2 do anything
        f = request.get('f') # from id
        t = request.get('t') # to id
        m = request.get('m') # message

        response = Element('u_spm')
        response.set('r', r)
        response.set('f', f)
        response.set('t', t)
        response.set('m', m)

        return response

    def handle_u_gsq(self, request):
        """Get Secure Question?"""
        pass

    def handle_u_acp(self, request):
        """Account Change Password"""
        pass

    def handle_u_afp(self, request):
        """Account Forgot Password"""
        pass

    def handle_u_rpm(self, request):
        """Receive Private Message"""
        pass

    def handle_u_gbl(self, request):
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

    def handle_u_abd(self, request):
        """Add Buddy"""
        buddy_name = request.get('n')

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

    def handle_u_abr(self, request):
        """Add Buddy Request"""
        b = '512' # id
        n = 'SOMEONEELSE' # name

        response = Element('u_abr')
        response.set('b', b)
        response.set('n', n)

        return response
        
    def handle_u_dbd(self, request):
        """Delete Buddy"""
        pass

    def handle_u_dbr(self, request):
        """Delete Buddy Request"""
        pass

    def handle_u_fbd(self, request):
        """Flag? Buddy"""
        pass

    def handle_u_ccs(self, request):
        """Chat Status (Buddy's chat status?)"""
        new_status = request.get('s') # can take values 0 for ready to party or 1 for dnd
        user_id = '2734650'

        response = Element('u_ccs')
        response.set('id', user_id)
        response.set('s', new_status)

        return response   

    def handle_u_cph(self, request):
        """Change Phone Status"""
        ph_in = request.get('ph')

        user_id = '2734650'
        ph_out = ph_in

        response = Element('u_cph')
        response.set('u', user_id)
        response.set('ph', ph_out)

        return response

    def handle_u_cos(self, request):
        """Change Online Status"""
        pass

    def handle_u_gcb(self, request):
        """Get Coin Balance"""
        pass

    # Appears to not be implemented
    def handle_u_gth(self, request):
        """Get Transaction History"""
        pass

    def handle_u_inv(self, request):
        """Invitation"""
        pass

    def handle_u_inr(self, request):
        """Invitaation Response"""
        pass

    def handle_u_p(self, request):
        """Ping"""
        t = '1'

        response = Element('u_p')
        response.set('t', t)
        
        return response

    def handle_p(self, request):
        """Ping"""
        t = '1'

        response = Element('p')
        response.set('t', t)
        
        return response