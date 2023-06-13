import datetime
import hashlib
import json
from datetime import datetime

import pytz
import requests
import telebot

# pip install pyTelegramBotAPI

bot = telebot.TeleBot("6049539925:AAGdnzKctyTGs5SKuiQQdO5GuQ6mbU7xFus")

authes = {}


@bot.message_handler(content_types=['text'])
def start(message):
    request_code = hashlib.md5(
        str(datetime.now(pytz.timezone('GMT')).replace(second=0, microsecond=0)).split('+')[0].encode('utf-8')
    ).hexdigest()[-5:]
    req = requests.get(f'http://localhost/getUser.php?request_code={request_code}&user={message.text}').text
    try:
        x = json.loads(req)
        if x:
            code = hashlib.md5(
                (str(
                    datetime.now(pytz.timezone('GMT')).replace(second=0, microsecond=0)
                ).split('+')[0]
                 + x['username']).encode('utf-8')
            ).hexdigest()[-5:]
            bot.send_message(message.from_user.id, str(
                datetime.now(pytz.timezone('GMT')).replace(second=0, microsecond=0)
            ).split('+')[0]
            + x['username'])
            bot.send_message(message.from_user.id, f"Welcome, {x['fullname']}!\nYour code: {code}")
            authes[message.from_user.id] = x['fullname']
    except:
        pass


bot.polling(none_stop=True, interval=0)
