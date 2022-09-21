from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters


updater = Updater("5571019908:AAEqq_-fzC5p-lz44h2-dSFbtJ6jQ2q9D2c",
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Cyber Hello!")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("This is help")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
