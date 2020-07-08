import discord
import random
import os

from plugins import *

class Tokusentai(discord.Client):
    last_channel = None
    plugins = []
    plugin_path = os.path.abspath('./plugins')

    async def on_ready(self):
        self.plugins = list(
            map(
                lambda func: eval(func, None, dict(self=self)),
                map(
                    lambda filename: filename.replace('.py', '(self)'),
                    os.listdir('./plugins')
                )
            )
        )



        self.plugins = list(map(
            self.create_instance_of,
            self.plugins
        ))

        print('Logged in {0}' . format(self.user))

    def create_instance_of(self, plugin):
        os.chdir(self.plugin_path + '/' + plugin.__name__)
        return plugin(self)

    async def on_message(self, message):
        self.last_channel = message.channel
        print('{0.author}: {0.content}' . format(message))
        return await self.respond(message)

    async def respond(self, message):
        if self.user.id == message.author.id:
            return

        response = ''

        plugins = sorted(
            list(
                filter(
                    lambda plugin,message=message: plugin.wants_to_respond(message),
                    self.plugins
                )
            ),
            key=lambda plugin: plugin.priority
        )

        if not plugins:
            plugins = []

        for plugin in plugins:
            if plugin.wants_to_respond(message):
                response = response + '\n' + self.get_string_response(plugin.get_response(message))
                if not plugin.allow_others:
                    break

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
