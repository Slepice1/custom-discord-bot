#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

from command_bot import CommandBot
from swear_bot import SwearBot
from loging_bot import LogingBot
from bots import Bots
from stats import Stats

config = {"trigger":"!",
          "images_locations": ("../images/{}.png", "../images/{}.gif"),
          "stats_location": "/home/slepice1/data.data",
          "db_location": "../messages.db",
          "server_id": "132560448775127041",
          "channels": ("lol", "test"),
          "message_to_db_count": 10}

stats = Stats(config)
command_bot = CommandBot(stats, config)
swear_bot = SwearBot(stats, config)
loging_bot = LogingBot(config)
bots = Bots([command_bot, swear_bot, loging_bot], config)

with open("login.data", 'r') as f:
    email, password = f.read().strip().split("\n")


bots.run(email, password)
