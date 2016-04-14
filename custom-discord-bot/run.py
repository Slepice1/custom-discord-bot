#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

from command_bot import CommandBot
from swear_bot import SwearBot
from loging_bot import LogingBot
from bots import Bots
from stats import Stats

config = {"trigger":"!",
          "images_location": "../data/images/",
          "images_types": ("{}.png", "{}.gif"),
          "stats_location": "../data/stats.data",
          "db_location": "../data/messages.db",
          "login_info_location": "../data/login.data",
          "server_id": "132560448775127041",
          "channels": ("lol"),
          "message_to_db_count": 20}

stats = Stats(config)
command_bot = CommandBot(stats, config)
swear_bot = SwearBot(stats, config)
loging_bot = LogingBot(config)
bots = Bots([command_bot, swear_bot, loging_bot], config)

with open(config["login_info_location"], 'r') as f:
    data = f.read().strip().split("\n")

bots.run(*data)
