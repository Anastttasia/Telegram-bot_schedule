import time
from datetime import datetime

from telebot.types import Message
from telebot import types

from loader import bot
from config import DEFAULT_COMMANDS


# TODO: посмотреть\удалить
# @bot.message_handler(content_types=['text'])
# def bot_message(message):
#     if message.chat.type == 'private':
#         if message.text == 'Помощь':
#             text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
#             bot.reply_to(message, "\n".join(text))




# запустить бота
@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item_help = types.KeyboardButton('Помощь')
    # item_user_id = types.KeyboardButton('Идентификация пользователя')
    # item_sign_to_mailing = types.KeyboardButton("Подписаться на рассылку расписания")
    # markup.add(item_help, item_user_id, item_sign_to_mailing, row_width=2)

    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}! Я пока нахожусь в разработке, но уже очень скоро смогу высылать тебе '
                     'актуальное расписание твоей группы'.format(
                         message.from_user),
                     reply_markup=markup
                     )

# Получить список команд
@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))


# Единоразово получить расписание
@bot.message_handler(commands=["get_schedule"])
def get_schedule(message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     "Идеальное расписание",
                     reply_markup=markup
                     )


# Подписаться на рассылку сообщений
@bot.message_handler(commands=["sign_into"])
def sign_to_income_messages(message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item_help = types.KeyboardButton('Помощь')
    # item_user_id = types.KeyboardButton('Идентификация пользователя')
    # item_sign_out_to_mailing = types.KeyboardButton("Отписаться от рассылки")
    # markup.add(item_help, item_user_id, item_sign_out_to_mailing, row_width=2)
    bot.send_message(message.chat.id,
                     "Готово! Теперь ты каждый день будешь получать расписание на завтра!",
                     reply_markup=markup
                     )
    while True:
        now = datetime.now()
        curr_time = now.strftime("%H:%M")
        if curr_time == '00:50':
            bot.send_message(message.chat.id,
                             'Ваше прекрасное расписание',
                             reply_markup=markup
                             )
            time.sleep(60)
        time.sleep(5)


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "Я не понимаю эту команду.\n" f"Сообщение: {message.text}. Список команд /help"
    )
