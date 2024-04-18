from loader import bot
import handlers  # noqa
from config import set_default_commands

if __name__ == "__main__":
    set_default_commands(bot)
    print('polling...')
    bot.infinity_polling()
