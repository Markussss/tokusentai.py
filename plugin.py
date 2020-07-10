class Plugin:
    priority = 0
    allow_others = True
    provide_files = False

    def __init__(self, client):
        self.client = client
