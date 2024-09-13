import telebot
import requests
import buttons as bt
import database as db
from geopy.geocoders import Photon

from buttons import back_in

bot = telebot.TeleBot(token='7234156924:AAGFVYKeIdAgkcY8byWjcZZf9mEUx7IO18U')
geolocator = Photon(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, 'Напиште сумму конвертации')
        bot.register_next_step_handler(message, convert)
    elif checker == False:
        bot.send_message(user_id, 'Добро пожаловать, это бот конвертер валют')
        bot.send_message(user_id, 'Напишите свое имя')
        bot.register_next_step_handler(message, get_name)
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Поделитесь своими контактами', reply_markup=bt.phone_number_bt())
    bot.register_next_step_handler(message, get_number, name)
def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        num = message.contact.phone_number
        bot.send_message(user_id, 'Поделитесь своим местоположением', reply_markup=bt.location_bt())
        db.add_user(name, num, user_id)
        bot.register_next_step_handler(message, get_location)
    else:
        bot.send_message(user_id, 'Отправьте свой номер через кнопку в меню', reply_markup=bt.phone_number_bt())
        bot.register_next_step_handler(message, get_number, name)
def get_location(message):
    user_id = message.from_user.id
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        address = geolocator.reverse((latitude, longitude)).address
        print(address)

    bot.send_message(user_id, 'Вы успешно прошли регистрацию')
    bot.send_message(user_id, 'Напишите сумму конвертации')
    bot.register_next_step_handler(message, convert)


@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Напишите сумму и бот сконвертирует её из UZS в USD, EUR и RUB')
    bot.register_next_step_handler(message, convert)

def convert(message):
    user_id = message.from_user.id
    text = message.text.strip() #удаление пробелов по краям
    try: #проверка ошибок
        sum = float(text)
    except ValueError:
        bot.send_message(user_id, 'Отправьте сумму', reply_markup=back_in())
        bot.register_next_step_handler(message, convert)
        return

    url = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
    USD = requests.get(url).json()
    bot.send_message(user_id, sum/float(USD[0]['Rate']))
    # uzs_rub = sum * 0.0073
    # uzs_usd = sum * 0.000079
    # uzs_eur = sum * 0.000071
    # bot.send_message(user_id, f'{sum} UZS = \n'
    #                  f'{uzs_rub:.2f} RUB\n'
    #                  f'{uzs_usd:.2f} USD\n'
    #                  f'{uzs_eur:.2f} EUR')
    bot.register_next_step_handler(message, convert)

@bot.callback_query_handler(func=lambda call: call)
def back(call):
    if call.data == "back":
        bot.clear_step_handler(call.message)
        bot.send_message(call.from_user.id, "Команды работают")
bot.infinity_polling()