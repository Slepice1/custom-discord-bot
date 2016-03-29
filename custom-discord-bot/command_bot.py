# -*- coding: utf-8 -*-

import os
import asyncio
from stats import Stats, MemberException

def command(func):
    func.command = None
    return func

class CommandBot():

    def __init__(self, stats_, config):
        self.config = config
        self.stats_ = stats_
        self.commands = []
        for k, v in CommandBot.__dict__.items():
            if hasattr(v, 'command'):
                self.commands.append(k)

    def on_message(self, msg):
        self.stats_.set_members(msg.server.members)
        if not msg.content.startswith(self.config['trigger']): return

        line = msg.content[len(self.config['trigger']):].lower()
        if ' ' in line:
            cmd, arg = line.split(' ', 1)
        else:
            cmd, arg = line, None

        if cmd not in self.commands: return
        func = getattr(self, cmd)
        try:
            return func(msg, arg)
        except MemberException as e:
            return [("send_message",(msg.channel, e))]

    def on_ready(self):
        print('Command bot running!')

    @command
    def bodik(self, msg, arg):
        if arg is not None:
            if msg.author.name.lower() != arg:
                self.stats_[arg]["bodik"] += 1
            else:
                return [("send_message",(msg.channel, "Sám si dát bodík nemůžeš :frowning:"))]
        else:
            return [("send_message",(msg.channel, "Potřebuji jméno komu mám dat bodik"))]

    @command
    def stats(self, msg, arg):
        if arg is not None:
            return [("send_message",(msg.channel, self.stats_.get_user_stats_str(arg)))]
        else:
            return [("send_message",(msg.channel, self.stats_.get_all_stats_str()))]

    @command
    def react(self, msg, arg):
        arg = arg.replace(".","").replace("/","")
        for location in self.config["images_locations"]:
            file_name = location.format(arg)
            if os.path.isfile(file_name):
                return [("send_file", (msg.channel, file_name), {"content":msg.author.name}),
                        ("delete_message", (msg,))]
        return [("send_message",(msg.channel, "Tato reakce neexistuje :frowning:"))]
