# -*- coding: utf-8 -*-

import asyncio
from stats import Stats, MemberException

class SwearBot():

    def __init__(self, stats_, config):
        self.config = config
        self.stats_ = stats_
        self.swear_words = self.build_swear_list()

    def on_message(self, msg):
        text = msg.content.lower()
        try:
            count = sum((text.count(word) for word in self.swear_words))
            if count > 0:
                self.stats_[msg.author.name]["sproste zpravy"] += 1
                self.stats_[msg.author.name]["sproste slova"] += count
        except MemberException as e:
            return e

    def on_ready(self):
        print('Swear bot running!')

    def build_swear_list(self):
        with open("../swear/cs", encoding="utf-8") as cs, \
             open("../swear/en", encoding="utf-8") as en:
              return cs.read().strip().split("\n") + \
                     en.read().strip().split("\n")
