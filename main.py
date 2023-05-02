from bs4 import BeautifulSoup as bs
import requests
import telebot

bot = telebot.TeleBot("key here")

languages = {
    "english": "Enter a word, or type /stop",
    "german": "Geben Sie ein Wort ein, oder schreiben Sie /stop ein",
    "russian": "Введите слово, или введите /stop"
}

invalid_word = {
    "english": "Invalid word, please try again, or type /stop",
    "german": "Ungültiges Wort, bitte versuchen Sie es erneut, oder schreiben Sie /stop ein",
    "russian": "Неверное слово, попробуйте еще раз, или введите /stop"
}

der_die_das = ["der", "die", "das"]

entering_word = [False]
language = [""]


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('English', callback_data='lang-english')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Russian', callback_data='lang-russian')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('German', callback_data='lang-german'),
    )
    bot.send_message(message.chat.id, "Please choose a language", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Type:\n"
                                      "/start, to start the Bot\n"
                                      "/help, to view help message\n"
                                      "/stop, to pause the Bot")


@bot.message_handler(commands=['stop'])
def stop(message):
    entering_word[0] = False
    bot.send_message(message.chat.id, "The chat is paused. To reactivate, type in /start or /help")


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('lang-'):
        bot.answer_callback_query(query.id)
        entering_word[0] = True
        language[0] = query.data[5:]
        bot.send_message(query.message.chat.id, languages[language[0]])
    else:
        print(query.message)


@bot.message_handler(regexp="(.*?)")
def handle_message(message):
    if entering_word[0]:
        artikel = get_artikel(message.text)
        if artikel == "":
            bot.send_message(message.chat.id, invalid_word[language[0]])
        else:
            bot.send_message(message.chat.id, "Artikel: " + artikel)


def get_artikel(word):
    result = ""
    for i in range(3):
        url = "https://der-artikel.de/{}/{}.html".format(der_die_das[i], word.capitalize())
        page = requests.get(url)
        data = bs(page.content, "html.parser")
        header = data.find(class_='masthead d-flex')
        try:
            header.find(class_='mb-1')
            result = der_die_das[i].capitalize()
            break
        except Exception:
            continue
    return result


bot.polling(none_stop=True)
