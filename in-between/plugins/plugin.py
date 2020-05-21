from xml.etree.ElementTree import Element

class Plugin:
    def __init__(self, plugin_id):
        self.plugin_id = plugin_id
        self.routes = {}
        self.user = None

    def handle_request(self, request):
        """Handle an xml request directed at the plugin and return an appropriate xml response."""
        route_id = request.tag
        route_handler = self.get_route(route_id)
        
        tag = f'h{self.plugin_id}_0'
        response = Element(tag)
        
        info = route_handler(request)
        if info is not None:
            response.append(info)

        return response

    def register_route(self, route_id, route_handler):
        self.routes[route_id] = route_handler

    def get_route(self, route_id):
        if route_id in self.routes:
            return self.routes[route_id]
        raise ValueError(f'No route with id {route_id} registered to plugin {self.id}')