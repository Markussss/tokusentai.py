class MyPlugin:
    def __init__(self, client):
        self.priority = 0
        self.allow_others = True

    def wants_to_respond(self, message):
        return True

    def get_response(self, message):
        return 'Hello world!'
