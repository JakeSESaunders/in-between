from plugins.plugin import Plugin
from xml.etree.ElementTree import Element

class PluginGalaxy(Plugin):
    def __init__(self, plugin_id):
        Plugin.__init__(self, plugin_id)
        self.register_route('lpv', self.handle_lpv)
        self.register_route('vsu', self.handle_vsu)
        self.register_route('sp', self.handle_sp)
        self.register_route('rr', self.handle_rr)
        self.register_route('profile', self.handle_profile)
        self.register_route('ge', self.handle_ge)
        self.register_route('gls', self.handle_gls)
        self.register_route('p', self.handle_p)

    def handle_lpv(self, request):
        # NOTE no params to get
        version = '0'

        response = Element('lpv')
        response.set('v', version)

        return response

    def handle_vsu(self, request):
        response = Element('vsu')

        return response

    def handle_sp(self, request):
        """Save Profile"""
        response = Element('sp')

        return response

    def handle_rr(self, request):
        response = Element('rr')

        return response

    def handle_profile(self, request):
        response = Element('profile')

        return response

    def handle_ge(self, request):
        response = Element('ge')

        return response

    def handle_gls(self, request):
        """Get Leaderboard Statistics"""
        stat_type = request.get('id') # 1 for games, 2 for items

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

    def handle_p(self, request):
        pass