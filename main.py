from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import requests
from bs4 import BeautifulSoup as bs
# import pandas as pd
import requests


updater = Updater("5571019908:AAEqq_-fzC5p-lz44h2-dSFbtJ6jQ2q9D2c", use_context=True)

languages = {
    "english": "Enter a word",
    "german": "Geben Sie ein Wort ein",
    "russian": "Введите слово"
}

der_die_das = ["der", "die", "das"]


class Handling:

    choose_lang = False
    enter_word = False
    language = ""

    def __init__(self):
        self.handle()

    def start(self, update: Update, context: CallbackContext):
        self.choose_lang = True
        update.message.reply_text("Please choose a language")

    def help(self, update: Update, context: CallbackContext):
        update.message.reply_text("This is help")

    def unknown_text(self, update: Update, context: CallbackContext):
        entered = update.message.text.lower()
        if self.choose_lang:
            if entered in languages:
                self.language = entered
                update.message.reply_text(languages[self.language])
                self.choose_lang = False
                self.enter_word = True
            else:
                update.message.reply_text("Please choose English, Russian or German")
        elif self.enter_word:
            update.message.reply_text(self.get_artikel(entered))

    def get_artikel(self, word):
        result = ""
        for i in range(3):
            url = "https://der-artikel.de/{}/{}.html".format(der_die_das[i], word.capitalize())
            page = requests.get(url)
            data = bs(page.content)
            header = data.find(class_='masthead d-flex')
            try:
                header.find(class_='mb-1')
                result = der_die_das[i].capitalize()
                break
            except Exception:
                continue
        return result

    ''' def unknown(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text) '''

    def handle(self):
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler('help', self.help))
        # updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
        # updater.dispatcher.add_handler(MessageHandler(
        # Filters.command, unknown))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.unknown_text))

        updater.start_polling()


Handling()
