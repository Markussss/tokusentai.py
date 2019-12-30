class NextPlugin:
    def __init__(self, client):
        self.priority = 0
        self.allow_others = False

    def wants_to_respond(self, message):
        return False

    def get_response(self, message):
        return 'Next'
