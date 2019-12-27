class MyPlugin:
    def want_to_respond_to(self, message):
        return True

    def get_response(self, message):
        return 'Hello world!'
