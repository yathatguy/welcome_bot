# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import logging
import os

from telegram.ext import Updater, Filters, MessageHandler

# from clients import log_client, check_username

STEP = 10
WELCOME_TEXT = 'Greetings, {}, welcome to AB-CHAIN community!'
MESSAGE_ID = 0

# Set up Updater and Dispatcher

updater = Updater(token=os.environ['TOKEN'])
updater.stop()
dispatcher = updater.dispatcher


def get_query(bot, update):
    if update.callback_query:
        query = update.callback_query
    else:
        query = update
    return query


def on_user_joins(bot, update):
    global MESSAGE_ID
    query = get_query(bot, update)
    if len(query.message.new_chat_members) > 0 and query.message.chat.type in ["group", "supergroup"]:
        logging.debug(query.message)
        if query.message.new_chat_member.username != None:
            text = WELCOME_TEXT.format(u'@' + query.message.new_chat_member.username)
        else:
            text = WELCOME_TEXT.format('stranger')
        bot.sendMessage(text=text, chat_id=query.message.chat.id)
        logging.info("Message {}, last info package was sent on greeting {}".format(query.message.message_id, MESSAGE_ID))
        if query.message.message_id > MESSAGE_ID + STEP:
            filedata = open("greeting.txt", "r")
            info_package = filedata.read()
            filedata.close()
            bot.sendMessage(text=info_package, chat_id=query.message.chat.id, disable_web_page_preview=True)
            MESSAGE_ID = query.message.message_id


def main():
    logging.basicConfig(level=logging.INFO)

    text_handler = MessageHandler(Filters.all, on_user_joins)
    dispatcher.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
