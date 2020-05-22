from plugins.plugin import Plugin
from xml.etree.ElementTree import Element
import data.trunk

class PluginTrunk(Plugin):
    def __init__(self, plugin_id):
        Plugin.__init__(self, plugin_id)
        self.register_route('gil', self.handle_gil)
        self.register_route('gcl', self.handle_gcl)
        self.register_route('grl', self.handle_grl)
        self.register_route('gfl', self.handle_gfl)
        self.register_route('gjl', self.handle_gjl)
        self.register_route('gml', self.handle_gml)
        self.register_route('glb', self.handle_glb)
        self.register_route('gut', self.handle_gut)
        self.register_route('gutc', self.handle_gutc)
        self.register_route('gsl', self.handle_gsl)
        self.register_route('te', self.handle_te)
        self.register_route('bi', self.handle_bi)
        self.register_route('bc', self.handle_bc)
        self.register_route('br', self.handle_br)
        self.register_route('bf', self.handle_bf)
        self.register_route('bm', self.handle_bm)
        self.register_route('bj', self.handle_bj)
        self.register_route('gua', self.handle_gua)
        self.register_route('p', self.handle_p)

    def handle_gil(self, request):
        """Get Items List"""
        response = Element('gil')

        return response

    def handle_gcl(self, request):
        """Get Cleanings? List"""
        url = 'localhost'

        response = Element('gcl')
        response.set('url', url)
        
        return response

    def handle_grl(self, request):
        """Get Rooms List"""
        response = Element('grl')

        return response

    def handle_gfl(self, request):
        """Get Familiars List"""
        url = 'localhost'

        response = Element('gfl')
        response.set('url', url)

        familiar_list = data.trunk.get_familiar_list()

        for familiar_data in familiar_list:
            familiar = Element('f')
            familiar.set('id', familiar_data.stack_id)
            familiar.set('rid', familiar_data.item_id)
            familiar.set('h', familiar_data.time)
            familiar.set('c', familiar_data.cost)
            familiar.set('dc', familiar_data.discounted_cost)
            familiar.set('d', familiar_data.discount)
            response.append(familiar)

        return response

    def handle_gjl(self, request):
        """Get Jammers List"""
        url = 'localhost'

        response = Element('gjl')
        response.set('url', url)

        jammer_list = data.trunk.get_jammer_list()

        for jammer_data in jammer_list:
            jammer = Element('j')
            jammer.set('id', jammer_data.stack_id)
            jammer.set('rid', jammer_data.item_id)
            jammer.set('q', jammer_data.quantity)
            jammer.set('c', jammer_data.cost)
            jammer.set('d', jammer_data.discount)
            response.append(jammer)

        return response

    def handle_gml(self, request):
        """Get Moods List"""
        url = 'localhost'

        response = Element('gml')
        response.set('url', url)

        return response

    def handle_glb(self, request):
        """Get Loot Balance"""
        loot_balance = '10000'

        response = Element('glb')
        response.set('b', loot_balance)

        return response

    def handle_gut(self, request):
        """Get User Transactions"""
        response = Element('gut')

        return response

    def handle_gutc(self, request):
        """Get User Transactions Count"""
        transaction_count = '1'

        response = Element('gutc')
        response.set('c', transaction_count)

        return response

    def handle_gsl(self, request):
        """Get Splash List"""
        response = Element('gsl')

        return response

    def handle_te(self, request):
        """Transaction Error"""
        response = Element('te')

        return response

    def handle_bi(self, request):
        """Buy Item"""
        response = Element('bi')

        return response

    def handle_bc(self, request):
        """Buy Cleaning?"""
        response = Element('bc')

        return response

    def handle_br(self, request):
        """Buy Room"""
        response = Element('br')

        return response

    def handle_bf(self, request):
        """Buy Familiar"""
        response = Element('bf')

        return response

    def handle_bm(self, request):
        """Buy Mood"""
        response = Element('bm')

        return response

    def handle_bj(self, request):
        """Buy Jammer"""
        database_id = request.get('id')
        new_balance = '75000'

        response = Element('bj')
        response.set('id', database_id)
        response.set('b', new_balance)
        
        return response

    def handle_gua(self, request):
        """Get User Asset"""
        response = Element('gua')

        return response

    def handle_asp(self, request):
        """Asset Parameters"""
        # for when a trunk jammer/familiar is used

        response = Element('asp')

        return response

    def handle_p(self, request):
        """Ping"""
        response = Element('p')

        return response
