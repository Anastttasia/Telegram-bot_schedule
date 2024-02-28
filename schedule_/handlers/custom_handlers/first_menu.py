from config_data.config import DEFAULT_COMMANDS
from handlers.default_handlers.help import bot_help
from loader import bot


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Помощь':
                text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
                bot.reply_to(message, "\n".join(text))
