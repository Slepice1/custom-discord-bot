# -*- coding: utf-8 -*-

import asyncio
import sqlite3
import datetime
import signal
import sys

class LogingBot():

    def __init__(self, config):
        self.config = config
        self.conn = sqlite3.connect(self.config["db_location"])
        self.db = self.conn.cursor()
        self.message_count = 0;
        def adapt_datetime(ts):
            return ts.timestamp()
        sqlite3.register_adapter(datetime.datetime, adapt_datetime)

        signal.signal(signal.SIGTERM, self.__del__)

    def __del__(self, *useless):
        self.conn.commit()
        sys.exit()

    def commit_if_enough(self):
        if self.message_count >= self.config["message_to_db_count"]:
            self.conn.commit()
            self.message_count = 0
        else:
            self.message_count += 1

    def on_message(self, msg):
        message = (msg.id, msg.author.id, msg.content, msg.timestamp)
        self.db.execute("""insert into messages (id, user_id, content, date_sent)
                           values (?, ?, ?, ?)""", message)
        self.commit_if_enough()

    def on_message_edit(self, msg_before, msg_after):
        message = (msg_after.content, msg_after.edited_timestamp, msg_before.id)
        self.db.execute("""update messages set content=?, date_edited=?
                           where id=?""", message)
        self.commit_if_enough()

    def on_message_delete(self, msg):
        message = (datetime.datetime.now(), msg.id)
        self.db.execute("""update messages set date_deleted=?
                           where id=?""", message)
        self.commit_if_enough()

    def on_ready(self):
        print('Loging bot running!')
