import os
from dotenv import load_dotenv, find_dotenv
from telebot.types import BotCommand
import loader

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("get_schedule", "Получить сегодняшнее расписание"),
    ("sign_into", "Подписаться на рассылку расписания")
)
