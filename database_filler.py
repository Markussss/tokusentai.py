import os
import discord
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

class DatabaseFiller(discord.Client):
    async def on_ready(self):
        print('Logged in {0}, filling database' . format(self.user))
        channels = list(map(lambda guild: guild.text_channels, self.guilds))
        channels = [item for sublist in channels for item in sublist]

        count = 0
        for channel in channels:
            async for message in channel.history(limit=200):
                async with channel.typing():
                    count = count + 1
                    print(count)
                    c.execute('''insert into messages values (?, ?, ?, ?)''', (
                        message.id, message.content, message.author.id, message.created_at))
                if count % 50 == 0:
                    conn.commit()
            await channel.send('done!')
            conn.commit()


conn = sqlite3.connect('tokusentai.db')
c = conn.cursor()

c.execute('''drop table if exists messages''')

c.execute('''create table if not exists messages
    (id int, message text, user text, date text)
''')

conn.commit()

bot = DatabaseFiller()
bot.run(os.getenv('TOKEN'))
