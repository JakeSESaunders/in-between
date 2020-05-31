from plugins.plugin import Plugin
from xml.etree.ElementTree import Element
from copy import copy
from data.volatile import userlist
from data.user.user import get_id, get_name

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

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_responses(self):
        responses = copy(self.responses)
        self.responses = []
        return responses

    def handle_u_gcl(self, request): # TODO
        """Get Currency List"""
        pass

    def handle_u_gwl(self, request): # TODO
        """Get Country List"""
        pass

    def handle_u_gul(self, request): # TODO
        """Get USA States List"""
        pass

    def handle_u_gfl(self, request): # TODO
        """Get File List"""
        pass

    def handle_u_reg(self, request):
        """Register"""
        name = request.get('l') # l for login name?
        password = request.get('p')
        client_id = request.get('c')
        affiliate_id = request.get('a')
        ad_id = request.get('d')
        answer = request.get('sa')
        question = request.get('sq')
        # TODO change r based on result of register_user
        r = '0' # can take values 0-5, 90 and 99
        # user_id = user.register_user(name, password, question, answer)

        response = Element('u_reg')
        response.set('r', str(r))
        response.set('u', str(user_id))

        return response

    def handle_u_sup(self, request): # TODO
        """Send Update Profile"""
        pass

    def handle_u_gup(self, request): # TODO
        """Get User Profile"""
        pass

    def handle_u_gsp(self, request): # TODO
        """Get Short Profile"""
        pass

    def handle_u_gus(self, request): # TODO
        """Get User Stats"""
        pass

    def handle_u_spm(self, request):
        """Send Private Message"""
        r = '0' # 0: OK, 1: OK, 2: OK, 3: Message isn't displayed
        f = request.get('f') # from id
        t = request.get('t') # to id
        m = request.get('m') # message

        response = Element('u_spm')
        response.set('r', str(r))
        response.set('f', str(f))
        response.set('t', str(t))
        response.set('m', str(m))

        # TODO check for existence of users, users logged in, buddy relation etc to affect r
        global userlist
        userlist.send_to_user_id(int(t), response)

        return response

    def handle_u_gsq(self, request): # TODO
        """Get Secure Question?"""
        pass

    def handle_u_acp(self, request): # TODO
        """Account Change Password"""
        pass

    def handle_u_afp(self, request): # TODO
        """Account Forgot Password"""
        pass

    def handle_u_rpm(self, request): # TODO
        """Receive Private Message"""
        pass

    def handle_u_gbl(self, request):
        """Get Buddy List"""
        r = '0' # can take values 0 or 1 TODO what do vals represent?

        response = Element('u_gbl')
        response.set('r', r)

        global userlist
        buddy_list = userlist.get_buddy_list(self.user_id)

        for buddy in buddy_list:
            buddy_data = Element('bd')
            buddy_data.set('id', str(buddy[0]))
            buddy_data.set('n', str(buddy[1]))
            buddy_data.set('o', str(buddy[2]))
            buddy_data.set('s', str(buddy[3]))
            buddy_data.set('bf', str(buddy[4]))
            buddy_data.set('cf', str(buddy[5]))
            buddy_data.set('ph', str(buddy[6]))

            response.append(buddy_data)

        return response

    def handle_u_abd(self, request):
        """Add Buddy"""
        buddy_name = request.get('n')

        # r takes values 0-8
        # 0: accepted immediately
        # 1: your user doesn't exist
        # 2: buddy with given name doesn't exist
        # 3: already your buddy
        # 4: decline
        # 5: offline
        # 6: adding yourself
        # 7: your list full
        # 8: their list full

        r = '0'

        name = get_name(self.user_id)
        if name is None:
            r = '1'
        buddy_id = get_id(buddy_name)
        if buddy_id is None:
            r = '2'
        if self.user_id == buddy_id:
            r = '6'

        global userlist
        user = userlist.get_user_from_id(self.user_id)
        if buddy_id in user.get_buddy_ids():
            r = '3'
        buddy = userlist.get_user_from_id(buddy_id)
        if buddy is None:
            r = '5'

        if r != '0':
            response = Element('u_abd')
            response.set('r', str(r))
            response.set('n', str(buddy_name))

            return response

        buddy_request = Element('u_abr')
        buddy_request.set('b', str(self.user_id))
        buddy_request.set('n', name)
        userlist.send_to_user_id(buddy_id, buddy_request)

    def handle_u_abr(self, request):
        """Add Buddy Response"""
        response_code = int(request.get('r')) # response 0: reject, 1 accept
        buddy_name = request.get('n') # name

        if response_code == 0:
            r = '4'
            response = Element('u_abd')
            response.set('r', r)
            response.set('n', buddy_name)

            return response
        if response_code == 1:
            global userlist
            user = userlist.get_user_from_id(self.user_id)
            buddy = userlist.get_user_from_name(buddy_name)

            print(user.name, buddy.name)
            user.add_buddy(buddy.user_id)
            
            user_response = Element('u_abd')
            user_response.set('r', '0')
            user_response.set('n', str(buddy.name))
            user_response.set('a', '0') # unknown
            user_response.set('b', str(buddy.user_id))
            user_response.set('o', str(buddy.online))
            user_response.set('s', str(buddy.status))
            user_response.set('bf', str(buddy.bf))
            user_response.set('cf', str(buddy.cf))
            user_response.set('ph', str(buddy.ph))

            buddy_response = Element('u_abd')
            buddy_response.set('r', '0')
            buddy_response.set('n', str(user.name))
            buddy_response.set('a', '0') # unknown
            buddy_response.set('b', str(user.user_id))
            buddy_response.set('o', str(user.online))
            buddy_response.set('s', str(user.status))
            buddy_response.set('bf', str(user.bf))
            buddy_response.set('cf', str(user.cf))
            buddy_response.set('ph', str(user.ph))
            
            userlist.send_to_user_id(buddy.user_id, buddy_response)
            return user_response
        
    def handle_u_dbd(self, request): # TODO
        """Delete Buddy"""
        buddy_id = int(request.get('b'))
        global userlist
        user = userlist.get_user_from_id(self.user_id)
        if user is not None:
            user.delete_buddy(buddy_id)

        response = Element('dbd')
        response.set('r', '0') # result code
        response.set('u', str(self.user_id))
        response.set('b', str(buddy_id))

        return response

    def handle_u_dbr(self, request): # TODO
        """Delete Buddy Request"""
        pass

    def handle_u_fbd(self, request): # TODO
        """Flag Buddy""" # NOTE updates a buddy's cf, bf details in buddy list with b as id
        pass

    def handle_u_ccs(self, request):
        """Chat Status (Buddy's chat status?)"""
        status = request.get('s') # can take values 0 for ready to party or 1 for dnd
        user_id = self.user_id

        global userlist
        userlist.change_chat_status(user_id, status)

        response = Element('u_ccs')
        response.set('id', str(user_id))
        response.set('s', str(status))

        return response

    def handle_u_cph(self, request):
        """Change Phone Status"""
        ph = request.get('ph')

        # TODO connect to db

        user_id = self.user_id

        response = Element('u_cph')
        response.set('u', str(user_id))
        response.set('ph', str(ph))

        return response

    def handle_u_cos(self, request): # NOTE redundant
        """Change Online Status"""
        pass

    def handle_u_gcb(self, request): # TODO
        """Get Coin Balance"""
        pass

    def handle_u_gth(self, request): # TODO appears not to be implemented
        """Get Transaction History"""
        pass

    def handle_u_inv(self, request): # TODO
        """Invitation"""
        pass

    def handle_u_inr(self, request): # TODO
        """Invitation Response"""
        pass

    def handle_u_p(self, request):
        """Ping"""
        t = '1'

        response = Element('u_p')
        response.set('t', str(t))
        
        return response

    def handle_p(self, request):
        """Ping"""
        t = '1'

        response = Element('p')
        response.set('t', str(t))
        
        return response