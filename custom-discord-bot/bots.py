
# -*- coding: utf-8 -*-

import asyncio
from discord import Client

class Bots(Client):

    def __init__(self, bots, config):
        Client.__init__(self)
        self.bots = bots
        self.config = config
        operations = [self.send_message, self.send_file, self.delete_message]
        self.operations = {op.__name__:op for op in operations}

    @asyncio.coroutine
    def _execute_and_react(self, function_name, *args):
        if args[0].channel.is_private: return
        if not self._is_in_our_group(args[0]): return
        if str(args[0].author) == "bot-autisti": return
        for bot in self.bots:
            func = getattr(bot, function_name, None)
            if callable(func):
                reactions = func(*args)
                if reactions is None: continue
                for reaction in reactions:
                    if len(reaction) < 3:
                        yield from self.operations[reaction[0]](*reaction[1])
                    else:
                        yield from self.operations[reaction[0]](*reaction[1], **reaction[2])

    def _is_in_our_group(self, msg):
        return msg.server.id == self.config["server_id"] and \
            msg.channel.name in self.config["channels"]

    @asyncio.coroutine
    def on_message(self, msg):
        yield from self._execute_and_react("on_message", msg)

    @asyncio.coroutine
    def on_message_edit(self, msg_before, msg_after):
        yield from self._execute_and_react("on_message_edit", msg_before, msg_after)

    @asyncio.coroutine
    def on_message_delete(self, msg):
        yield from self._execute_and_react("on_message_delete", msg)

    @asyncio.coroutine
    def on_ready(self):
        for bot in self.bots:
            func = getattr(bot, "on_ready", None)
            if callable(func):
                func()
