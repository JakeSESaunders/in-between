from xml.etree.ElementTree import Element

class Plugin:
    def __init__(self, plugin_id):
        self.plugin_id = plugin_id
        self.routes = {}
        self.user = None
        self.responses = []

    def handle_request(self, request):
        """Handle an xml request directed at the plugin and return an appropriate xml response."""
        route_id = request.tag
        route_handler = self.get_route(route_id)
        response = route_handler(request)
        if response is not None:
            self.queue_response(response)

    def register_route(self, route_id, route_handler):
        self.routes[route_id] = route_handler

    def get_route(self, route_id):
        if route_id in self.routes:
            return self.routes[route_id]
        raise ValueError(f'No route with id {route_id} registered to plugin {self.plugin_id}')

    def queue_response(self, response):
        self.responses.append(response)

    def get_responses(self):
        responses = []
        if len(self.responses) > 0:
            parent = Element(f'h{self.plugin_id}_0')
            for response in self.responses:
                parent.append(response)
            responses.append(parent)
            self.responses = []
        return responses