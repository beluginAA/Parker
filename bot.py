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

    mysql = Mysql()
    all_skills_lower = [skill.lower() for skill in mysql._get_skills()]

    if message.text in ['👋 Поздороваться', '🧠 Главное меню']:
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton('📍 Количество вакансий')
        btn2 = types.KeyboardButton('📋 Список всех навыков')
        btn3 = types.KeyboardButton('🧠 Главное меню')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '🗂 Введите интересующий вас запрос', reply_markup=markup)

    elif message.text == '📍 Количество вакансий':
        mysql = Mysql()
        result = mysql._get_vacancies_amount()
        bot.send_message(message.from_user.id, f'📍 Количество обработанных вакансий на данный момент: {result}')

    elif message.text == '📋 Список всех навыков':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton('📈 Популярные навыки')
        btn2 = types.KeyboardButton('📉 Непопулярные навыки') 
        btn3 = types.KeyboardButton('🗄 Информация о конкретном навыке')
        btn4 = types.KeyboardButton('🧠 Главное меню')
        markup.add(btn1, btn2, btn3, btn4)
        mysql = Mysql()
        skills_list, result = mysql._get_skills_with_letters(), ''
        bot.send_message(message.from_user.id, '🔎 Информацию о каком навыке вы хотели бы получить?\n📋 Вот список доступных навыков:')
        for letter, skills in skills_list.items():
            result += letter + '\n'
            for id in range(len(skills)):
                if id != len(skills) - 1:
                    result += skills[id] + ', '
                else:
                    result += skills[id]
            result += '\n\n' 
        bot.send_message(message.from_user.id, result)
        bot.send_message(message.from_user.id, '✏️ Введите интересующий вас запрос', reply_markup=markup)

    elif message.text == '📈 Популярные навыки':
        mysql = Mysql()
        popular_skills, result = mysql._get_most_popular_skills(), ''
        bot.send_message(message.from_user.id, '📋 Вот список самых популярных навыков на данный момент:')
        for row in popular_skills:
            result += row 
        bot.send_message(message.from_user.id, result)
    
    elif message.text == '📉 Непопулярные навыки':
        mysql = Mysql()
        nonpopular_skills, result = mysql._get_less_popular_skills(), ''
        bot.send_message(message.from_user.id, '📑 Вот список самых непопулярных навыков на данный момент:')
        for row in nonpopular_skills:
            result += row 
        bot.send_message(message.from_user.id, result)

    elif message.text == '🗄 Информация о конкретном навыке':
        bot.send_message(message.from_user.id, '📌 Введите навык, о котором вы бы хотели узнать.')
 

    elif message.text.lower() in all_skills_lower:
        bot.send_message(message.from_user.id, '📌 Введите навык')
    
    else:
        bot.send_message(message.from_user.id, '🫣 Я не знаю такой навык.\n🤨 Попробуйте ввести один из навыков из списка:')
        mysql = Mysql()
        skills_list, result = mysql._get_skills_with_letters(), ''
        for letter, skills in skills_list.items():
            result += letter + '\n'
            for id in range(len(skills)):
                if id != len(skills) - 1:
                    result += skills[id] + ', '
                else:
                    result += skills[id]
            result += '\n\n' 
        bot.send_message(message.from_user.id, result)

bot.polling(none_stop=True, interval=0)