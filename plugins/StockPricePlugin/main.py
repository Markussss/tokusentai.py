class StockPricePlugin:
    def __init__(self, client):
        self.priority = 0
        self.allow_others = True

    def wants_to_respond(self, message):
        """
        Boolean function that decides if this plugin should
        respond to the current message nor not.

        As this function will be run for all messages in
        the server, it's a good idea to keep the function
        as fast as possible.
        """
        return True

    def get_response(self, message):
        """
        The message response we want to send, based on the
        current message.
        """
        return 'Hello world from StockPricePlugin!'


