import discord
import yaml
import random
import os

from plugins import *

class Tokusentai(discord.Client):
    last_channel = None
    simple_messages = {}
    fuzzy_messages = {}
    direct_messages = {}
    plugins = []

    async def on_ready(self):
        with open('simple-messages.yml') as stream:
            self.simple_messages = yaml.load(stream)
        with open('simple-fuzzy-messages.yml') as stream:
            self.fuzzy_messages = yaml.load(stream)
        with open('simple-direct-messages.yml') as stream:
            self.direct_messages = yaml.load(stream)

        # get all files in plugins folder
        # replace .py with () in order to use it as object creators
        # evaluate class names from strings to objects
        # turn the map into a list
        self.plugins = list(
            map(
                lambda func: eval(func),
                map(
                    lambda filename: filename.replace('.py', '()'),
                    os.listdir('./plugins')
                )
            )
        )

        print('Logged in {0}' . format(self.user))

    async def on_message(self, message):
        self.last_channel = message.channel
        print('{0.author}: {0.content}' . format(message))
        return await self.respond(message)

    async def respond(self, message):
        if self.user.id == message.author.id:
            return

        response = None

        print(len(self.plugins))
        for plugin in self.plugins:
            print(plugin.get_response(message))
            if plugin.want_to_respond_to(message):
                response = self.get_string_response(plugin.get_response(message))

        if not response:
            response = self.get_response(message)

        if len(response) > 0:
            return await message.channel.send(response)

        return

    def get_string_response(self, response):
        if not response:
            return ''

        if isinstance(response, str):
            return response

        if isinstance(response, list):
            # get random
            return response[random.randint(0, len(response) - 1)]

        if isinstance(response, dict):
            # get weighted random
            weight = 0
            for possible_response in response:
                weight = weight + response[possible_response]
            selected = random.randint(0, weight)
            for possible_response in response:
                selected = selected - response[possible_response]
                if selected <= 0:
                    return possible_response
            return response

    def get_response(self, message):
        response = None
        if message.content.startswith('<@!{0.id}>' . format(self.user)):
            response = self.direct_messages[self.remove_mention(message.content)]

        if message.content in self.simple_messages:
            response = self.simple_messages[message.content]

        for trigger in self.fuzzy_messages:
            if trigger in message.content:
                response = self.fuzzy_messages[trigger]

        return self.get_string_response(response)

    def remove_mention(self, text):
        return text.replace('<@!{0.id}> ' . format(self.user), '').strip()
