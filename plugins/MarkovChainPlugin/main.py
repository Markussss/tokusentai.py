import os
import re
import random
import plugin
import sqlite3
import markovify

class MarkovChainPlugin(plugin.Plugin):
    provide_files = True

    def __init__(self, client):
        super().__init__(client)
        self.models = {}

        connection = sqlite3.connect('{0}.db' . format(os.getenv('NAME')))
        cursor = connection.cursor()

        uninteresting_patterns = [
            r':[@a-zA-Z0-9_-]+?:',
            r'<.*?>',
            r'https?://.*? ',
            r'@ ',
            ' ,',
        ]

        patterns_that_need_improvement = [
            (r' \.', '.'),
            (r'\.\.', '.'),
            (r' +', ' '),
            (r'\n', '. ')
        ]

        for author in cursor.execute('SELECT DISTINCT(author) FROM messages WHERE bot = 0 and ignore = 0').fetchall():
            text = '. '.join(
                list(
                    map(
                        lambda t: t[0],
                        cursor
                            .execute('SELECT message FROM messages WHERE author = ?', (author[0], ))
                            .fetchall()
                    )
                )
            )
            for pattern in uninteresting_patterns:
                text = re.sub(pattern, '', text)

            for (search, replace) in patterns_that_need_improvement:
                text = re.sub(search, replace, text)
            self.models[author[0]] = markovify.Text(text,  well_formed=False)

    def wants_to_respond(self, message):
        return message.content.startswith(os.getenv('NAME'))

    def get_response(self, message):
        author = message.author.id
        while author == message.author.id:
            author = random.choice(list(self.models))

        start = message.content.replace(os.getenv('NAME'), '').strip().split(' ')[0]
        message = None

        try:
            if start:
                message = self.models[author].make_sentence_with_start(start)

            if not message:
                message = self.models[author].make_short_sentence(350)

            if not message:
                return self.get_response(message)
            return message
        except:
            message = self.models[author].make_short_sentence(350)
            if message:
                return message
            return ''
