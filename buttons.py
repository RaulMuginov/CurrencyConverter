from telebot import types

def phone_number_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text='Поделится номером', request_contact=True)
    kb.add(button)
    return kb
def location_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text='Поделится локацией', request_location=True)
    kb.add(button)
    return kb

def back_in():
    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Назад', callback_data='back')
    kb.add(button)
    return kb
