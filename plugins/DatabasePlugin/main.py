import os
import plugin
import sqlite3

class DatabasePlugin(plugin.Plugin):
    provide_files = True
    priority = 10

    def __init__(self, client):
        self.connection = sqlite3.connect('{0}.db' . format(os.getenv('NAME')))
        self.cursor = self.connection.cursor()


    def wants_to_respond(self, message):
        self.cursor.execute('INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            message.id,
            message.content,
            message.author.id,
            message.author.name,
            message.channel.id,
            message.created_at,
            len(message.content),
            message.author.bot,
            0,
        ))
        self.connection.commit()
        return False
