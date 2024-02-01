import telebot
from telebot.types import Message, InputMediaPhoto
from service import GroupService

BOT_TOKEN = '6861667224:AAGDsa3MPTppB71FWzMQ4EhmYSjE0r8GJ6g'

bot = telebot.TeleBot(BOT_TOKEN)
group_service = GroupService()


@bot.message_handler(commands=['start'])
def send_test(message: Message):
    bot.send_message(message.chat.id, '''
    ''')


@bot.message_handler(commands=['subscribe'])
def subscribe(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, group_service.subscribe(chat_id))


@bot.message_handler(commands=['unsubscribe'])
def subscribe(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, group_service.unsubscribe(chat_id))


def send_cars(cars: list):


    for group_id in group_service.get_all_group_ids():
        bot.send_message(group_id, 'Test for newsletter')


@bot.message_handler()
def test(message: Message):
    photos = [InputMediaPhoto(
        'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/1200px-Image_created_with_a_mobile_phone.png',
        caption='Test caption'),
        InputMediaPhoto(
            'https://dfstudio-d420.kxcdn.com/wordpress/wp-content/uploads/2019/06/digital_camera_photo-1080x675.jpg')]
    bot.send_media_group(message.chat.id, photos)


def convert_to_media_group(photos: list, caption=''):
    media_group = []
    for index, photo in enumerate(photos):
        media_group.append(InputMediaPhoto(photo, caption=(caption if index == 0 else '')))

    return media_group


bot.infinity_polling()
