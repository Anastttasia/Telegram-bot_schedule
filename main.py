import telebot
import sqlite3
from db.schedule_db import ScheduleDB
from datetime import datetime, timedelta, date
import time

table_name = "Netology"
schedule = ScheduleDB()
schedule.createNewGroup(table_name)

# Токен вашего бота
BOT_TOKEN = "6324418773:AAGqLSzRvKJzSbO721xM2CS9O0TL1t5BrBc"

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

def get_schedule_scheduleDb(day_of_week):
    conn = sqlite3.connect(DATABASE_SCHEDULE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Netology WHERE date = ?", (day_of_week,))
    schedule_data = cursor.fetchall()
    conn.close()
    return schedule_data

def send_schedule_to_users():
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    today = days_of_week[datetime.today().weekday()]

    schedule_data = get_schedule_scheduleDb(today)

    if schedule_data:
        schedule_text = "Привет, твое расписание на сегодня:\n"
        for row in schedule_data:
            schedule_text += f"Day: {row[1]}\nTime: {row[2]}\nSubject: {row[3]}\nSubgroup: {row[4]}\nTeacher: {row[5]}\nLink: {row[6]}\n\n"
        for user_id in get_all_user_ids():
            try:
                bot.send_message(user_id, schedule_text)
                print(f"Расписание отправлено пользователю {user_id}")
            except telebot.apihelper.ApiException as e:
                print(f"Ошибка при отправке расписания пользователю {user_id}: {e}")
    else:
        print("На сегодня расписание отсутствует.")

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
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    today = days_of_week[datetime.today().weekday()]

    schedule_data = get_schedule_scheduleDb(today)

    if schedule_data:
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

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


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


