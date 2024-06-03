import telebot
import sqlite3
from datetime import datetime, timedelta, date
import time

# Токен вашего бота
BOT_TOKEN = "6324418773:AAG6oyjJXC6OlyDEQfSCJR1r6QpVZZQklOs"

# Название базы данных
DATABASE_NAME = "message.db"
DATABASE_SCHEDULE = "schedule.db"

bot = telebot.TeleBot(BOT_TOKEN)

def get_all_user_ids():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT id FROM message")
    user_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return user_ids


def get_schedule_scheduleDb(date):
    conn = sqlite3.connect(DATABASE_SCHEDULE)
    cursor = conn.cursor()
    date_string = date.strftime('%d-%m-%Y')
    cursor.execute("SELECT * FROM Netology WHERE date = ?", (date_string,))
    schedule_data = cursor.fetchall()
    if not schedule_data:  # Check if schedule_data is empty
        schedule_data = []  # Return an empty list
    conn.close()
    return schedule_data


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! 👋  Я бот, который может отправлять вам расписание.", reply_markup=generate_menu())

# Обработка команды /subscribe
@bot.message_handler(func=lambda message: message.text == "Подписаться на рассылку")
def subscribe_handler(message):
    bot.send_message(message.chat.id, "К какой группе вы относитесь?", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, handle_group_response)

def handle_group_response(msg):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    user_id = msg.chat.id
    group_name = msg.text
    cursor.execute("INSERT INTO message (id, name) VALUES (?, ?)", (user_id, group_name))
    conn.commit()
    conn.close()
    bot.send_message(msg.chat.id, "Вы успешно подписались на рассылку! 🎉", reply_markup=generate_menu())

# Обработка команды /show_schedule
@bot.message_handler(func=lambda message: message.text == "Показать расписание")
def show_schedule_handler(message):
    # Получаем текущую дату
    today = date.today()

    # Получаем расписание из базы данных
    schedule_data = get_schedule_scheduleDb(today)

    # Проверяем, есть ли записи в расписании для сегодняшней даты
    schedule_for_today = []
    for row in schedule_data:
        schedule_date = datetime.strptime(row[1], '%d-%m-%Y').date()
        if schedule_date == today:
            schedule_for_today.append(row)

    # Формируем сообщение
    if schedule_for_today:
        schedule_text = "Привет, твое расписание на сегодня:\n"
        for row in schedule_data:
            schedule_text += f"День: {row[1]}\nВремя: {row[2]}\nПредмет: {row[3]}\nОписание: {row[4]}\nГруппа: {row[5]}\nПреподаватель: {row[6]}\nСсылка: {row[7]}\n\n"
        m = schedule_text
        if len(m) > 4095:
            for x in range(0, len(m), 4095):
                bot.reply_to(message, text=m[x:x + 4095])
        else:
            bot.reply_to(message, text=m)
    else:
        bot.send_message(message.chat.id, "На сегодня расписание отсутствует. 🤔", reply_markup=generate_menu())


# Обработка команды /help
@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_handler(message):
    bot.send_message(message.chat.id, "Я могу отправлять вам расписание каждый день в 9:00 утра.\n\nВы можете подписаться на рассылку, чтобы получать расписание, или просто посмотреть его прямо сейчас.\n\nИспользуйте кнопки ниже для взаимодействия со мной.", reply_markup=generate_menu())

def generate_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Подписаться на рассылку", "Показать расписание")
    keyboard.row("Помощь")
    return keyboard

conn = sqlite3.connect("message.db")

# Создаем курсор
cursor = conn.cursor()

# Создаем таблицу

cursor.execute("CREATE TABLE IF NOT EXISTS message (id INTEGER PRIMARY KEY, name TEXT)")

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()


# Запускаем функцию рассылки
if __name__ == "__main__":
    generate_menu()
    bot.polling()


