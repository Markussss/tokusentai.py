import plugin

class NextPlugin(plugin.Plugin):
    def __init__(self, client):
        super().__init__(client)

    def wants_to_respond(self, message):
        return False

    def get_response(self, message):
        return 'Next'
