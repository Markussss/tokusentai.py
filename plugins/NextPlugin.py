class NextPlugin:
    def want_to_respond_to(self, message):
        return False

    def get_response(self, message):
        return 'Next'
