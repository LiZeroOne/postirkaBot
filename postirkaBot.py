import telebot
from telebot import types
from config import token
from datetime import date, time, timedelta
import re
import db

bot = telebot.TeleBot(token)
db.create_table()
user_data = []
record_data = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton('Регистрация')
    markup.add(button)
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Регистрация')
def registration(message):
    user_data.clear()
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'Напиши Свое имя:', reply_markup=markup)
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    #user_data[message.from_user.id] = {'name': message.text}
    user_data.append(message.from_user.id)
    user_data.append(message.text)

    bot.send_message(message.chat.id, 'Напиши Свою комнату:')
    bot.register_next_step_handler(message, get_room)


def get_room(message):
    room = re.search(r'\d+', message.text)
    if room and room.group() != '0':
        #user_data[message.from_user.id]['room'] = room.group()
        user_data.append(room.group())
        db.insert_user(tuple(user_data))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('Записаться на постирку')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Запомнил!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')


@bot.message_handler(func=lambda message: message.text == 'Записаться на постирку')
def enroll(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button2 = types.KeyboardButton('На сегодня')
    button3 = types.KeyboardButton('На завтра')
    markup.add(button2, button3)
    bot.send_message(message.chat.id, 'Выбери день:', reply_markup=markup)
    bot.register_next_step_handler(message, get_time)


def get_time(message):

    if message.text == 'На сегодня':
        #user_data[message.from_user.id] = {'time': date.today()}
        record_data.append(date.today())
        record_data.append(message.from_user.id)
        db.insert_record(tuple(record_data))
    elif message.text == 'На завтра':
        #user_data[message.from_user.id] = {'time': date.today() + timedelta(days=1)}
        record_data.append(date.today() + timedelta(days=1))
        record_data.append(message.from_user.id)
        db.insert_record(tuple(record_data))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button2 = types.KeyboardButton('На час')
    button3 = types.KeyboardButton('На два часа')
    button4 = types.KeyboardButton('На три часа')
    markup.add(button2, button3, button4)
    bot.send_message(message.chat.id, 'Выбери время:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    #if room != 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Записаться на постирку")
        button2 = types.KeyboardButton("Журнал")
        button3 = types.KeyboardButton("Убрать запись")
        button4 = types.KeyboardButton("Помощь")
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, reply_markup=markup)
    #else:
        bot.send_message(message.from_user.id, 'На этаже нет комнаты с номером 0')


bot.polling(none_stop=True)
