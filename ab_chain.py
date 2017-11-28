# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import logging
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
        if query.message.chat.username != None:
            text = WELCOME_TEXT.format(query.message.chat.username)
        else:
            text = WELCOME_TEXT.format('stranger')
        bot.sendMessage(text=text, chat_id=query.message.chat.id)
        MESSAGE_ID = query.message.message_id
    if query.message.message_id > MESSAGE_ID + STEP:
        filedata = open("greeting.txt", "r")
        infoPackage = filedata.read()
        filedata.close()
        bot.sendMessage(text=infoPackage, chat_id=query.message.from_user.id, disable_web_page_preview=True)


def main():

    logging.basicConfig(level=logging.WARN)

    text_handler = MessageHandler(Filters.all, on_user_joins)
    dispatcher.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':

    main()
