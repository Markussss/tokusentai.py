import yaml

class YamlPlugin:
    def __init__(self, client):
        self.priority = 0
        self.allow_others = True
        self.client = client

        with open('simple-messages.yml') as stream:
            self.simple_messages = yaml.load(stream, Loader=yaml.FullLoader)
        with open('simple-fuzzy-messages.yml') as stream:
            self.fuzzy_messages = yaml.load(stream, Loader=yaml.FullLoader)
        with open('simple-direct-messages.yml') as stream:
            self.direct_messages = yaml.load(stream, Loader=yaml.FullLoader)

    def wants_to_respond(self, message):
        return (
            self.is_mentioned(message) or
            message.content in self.simple_messages or
            self.trigger_in_fuzzy_messages(message)
        )

    def get_response(self, message):
        response = ''
        if message.content.startswith('<@!{0.id}>' . format(self.client.user)):
            response = self.direct_messages[self.remove_mention(message.content)]

        if message.content in self.simple_messages:
            response = self.simple_messages[message.content]

        for trigger in self.fuzzy_messages:
            if trigger in message.content:
                response = self.fuzzy_messages[trigger]

        return response

    def remove_mention(self, text):
        return text.replace('<@!{0.id}> ' . format(self.client.user), '').strip()

    def is_mentioned(self, message):
        return '<@!{0.id}>' . format(self.client.user) in message.content

    def trigger_in_fuzzy_messages(self, message):
        for trigger in self.fuzzy_messages:
            if trigger in message.content:
                return True
        return False

    def test(self):
        return 'Test YamlPlugin'
