import telebot

from telebot import types
from config import bot_token, url_grafana
from mysql import Mysql

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Ссылка на grafana')
        btn2 = types.KeyboardButton('Информация от БД')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота

    elif message.text == 'Ссылка на grafana':
        keyboard = types.InlineKeyboardMarkup()
        key_grafana = types.InlineKeyboardButton(text='Ссылка на grafana', callback_data='grafana', url=url_grafana) #кнопка «Да»
        keyboard.add(key_grafana); #добавляем кнопку в клавиатуру
        bot.send_message(message.from_user.id, text='📊 Ссылка на dashboard grafana:', reply_markup=keyboard)

    elif message.text == 'Информация от БД':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Количество вакансий')
        btn2 = types.KeyboardButton('Популярные навыки')
        btn3 = types.KeyboardButton('Непопулярные навыки')
        btn4 = types.KeyboardButton('Информация по конкретному навыку')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, '🗂 Введите интересующий вас запрос', reply_markup=markup)

    elif message.text == 'Количество вакансий':
        mysql = Mysql()
        result = mysql._get_vacancies_amount()
        bot.send_message(message.from_user.id, f'📍 Количество обработанных вакансий на данный момент: {result}')

    elif message.text == 'Популярные навыки':
        mysql = Mysql()
        popular_skills, result = mysql._get_most_popular_skills(), ''
        bot.send_message(message.from_user.id, '📋 Вот список самых популярных навыков на данный момент:')
        for row in popular_skills:
            result += row 
        bot.send_message(message.from_user.id, result)
    
    elif message.text == 'Непопулярные навыки':
        mysql = Mysql()
        nonpopular_skills, result = mysql._get_less_popular_skills(), ''
        bot.send_message(message.from_user.id, '📑 Вот список самых непопулярных навыков на данный момент:')
        for row in nonpopular_skills:
            result += row 
        bot.send_message(message.from_user.id, result)

    elif message.text == 'Информация по конкретному навыку':
        bot.send_message(message.from_user.id, '🔎 Информацию о каком навыке вы хотели бы получить?')

# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == 'grafana': 
#         bot.send_message(call.from_user.id, 'Docker-контейнер с grafana доступен по ')
    # elif call.data == "no":
    #     bot.send_message(call.message.chat.id, 'Это печально')


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# @bot.message_handler(commands=['start'])
# def start(message):

#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton("🇷🇺 Русский")
#     btn2 = types.KeyboardButton('🇬🇧 English')
#     markup.add(btn1, btn2)
#     bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)
# name = ''
# surname = ''
# age = 0
# @bot.message_handler(content_types=['text'])
# def start(message):
#     if message.text == '/reg':
#         bot.send_message(message.from_user.id, "Как тебя зовут?")
#         bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
#     else:
#         bot.send_message(message.from_user.id, 'Напиши /reg')

# def get_name(message): #получаем фамилию
#     global name
#     name = message.text
#     bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
#     bot.register_next_step_handler(message, get_surname)

# def get_surname(message):
#     global surname
#     surname = message.text
#     bot.send_message(message.from_user.id, 'Сколько тебе лет?')
#     bot.register_next_step_handler(message, get_age)

# def get_age(message):
#     global age
#     while age == 0: #проверяем что возраст изменился
#         try:
#              age = int(message.text) #проверяем, что возраст введен корректно
#         except Exception:
#              bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
#     keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
#     key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
#     keyboard.add(key_yes); #добавляем кнопку в клавиатуру
#     key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
#     keyboard.add(key_no)
#     question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?'
#     bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)