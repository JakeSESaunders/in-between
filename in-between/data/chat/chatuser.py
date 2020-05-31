class Chatuser:
    def __init__(self, user_id, name, funkey_id, dl, handler):
        self.user_id = user_id
        self.name = name
        self.funkey_id = funkey_id
        self.dl = dl
        self.handler = handler

    def player_details(self):
        """Return a tuple of the user's details."""
        return (self.user_id, self.name, self.funkey_id, self.dl)

    def send(self, xml_message):
        """Send an xml message to the user."""
        self.handler.queue_response(xml_message)