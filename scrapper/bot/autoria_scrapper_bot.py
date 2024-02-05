import telebot
from telebot.types import Message, InputMediaPhoto
from scrapper.service.group_service import GroupService
import threading

__BOT_TOKEN = '6861667224:AAGDsa3MPTppB71FWzMQ4EhmYSjE0r8GJ6g'
__group_service = GroupService()
bot = telebot.TeleBot(__BOT_TOKEN)


def send_car(chat_id, media: list[InputMediaPhoto]):
    bot.send_media_group(chat_id, media)


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, '''
Привіт! Це бот для відслідковування нових пропозицій про авто
/subscribe - Для того, щоб підпіситась на оновлення
/unsubscribe - Для того, щоб відписатись від оновлень 
    ''')


@bot.message_handler(commands=['subscribe'])
def subscribe(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, __group_service.subscribe(chat_id))


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, __group_service.unsubscribe(chat_id))


bot_thread = threading.Thread(target=bot.infinity_polling, name='TgBot')
bot_thread.start()
