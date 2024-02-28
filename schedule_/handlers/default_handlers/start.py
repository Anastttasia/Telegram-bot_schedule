from telebot.types import Message

from loader import bot
from telebot import types

@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton('Помощь')
    item2 = types.KeyboardButton('Идентификация пользователя')
    markup.add(item1, item2)
    bot.send_message(message.chat.id,'Привет, {0.first_name}! Я пока нахожусь в разработке, но уже очень скоро смогу высылать тебе актуальное расписание твоей группы'.format(message.from_user), reply_markup=markup)
