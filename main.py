import telebot
import sqlite3
from db.schedule_db import ScheduleDB
from datetime import datetime, date

table_name = "Netology"
schedule = ScheduleDB()
schedule.createNewGroup(table_name)

# Токен вашего бота
BOT_TOKEN = "6324418773:AAEIWge54hrrxGvRnJepfgLC4y7u_A7Me_A"

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

def get_schedule_scheduleDb(date, groupId):
    conn = sqlite3.connect(DATABASE_SCHEDULE)
    cursor = conn.cursor()
    date_string = date.strftime('%d-%m-%Y')
    cursor.execute("SELECT * FROM Netology WHERE date = ? AND subgroup_number = ?", (date_string, groupId))
    schedule_data = cursor.fetchall()
    if not schedule_data:  # Check if schedule_data is empty
        schedule_data = []  # Return an empty list
    conn.close()
    return schedule_data

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! 👋  Я бот, который может отправлять вам расписание.", reply_markup=generate_menu())

@bot.message_handler(func=lambda message: message.text == "Подписаться на рассылку")
def subscribe_handler(message):
    bot.send_message(message.chat.id, "К какой группе вы относитесь?", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, handle_group_response)

def handle_group_response(msg):
    user_id = msg.chat.id
    group_name = msg.text
    insert_or_update_user(user_id, group_name)
    bot.send_message(msg.chat.id, "Вы успешно подписались на рассылку! 🎉", reply_markup=generate_menu())
@bot.message_handler(func=lambda message: message.text == "Показать расписание")
def show_schedule_handler(message):
    conn_message = sqlite3.connect(DATABASE_NAME)
    cursor_message = conn_message.cursor()
    cursor_message.execute("SELECT name FROM message WHERE id = ?", (message.chat.id,))
    group_name = cursor_message.fetchone()[0]

    today = date.today()

    schedule_data = get_schedule_scheduleDb(today, group_name)

    schedule_for_today = []
    for row in schedule_data:
        schedule_date = datetime.strptime(row[1], '%d-%m-%Y').date()
        if schedule_date == today:
            schedule_for_today.append(row)

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

@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_handler(message):
    bot.send_message(message.chat.id, "Я могу отправлять вам расписание каждый день в 9:00 утра.\n\nВы можете подписаться на рассылку, чтобы получать расписание, или просто посмотреть его прямо сейчас.\n\nИспользуйте кнопки ниже для взаимодействия со мной.", reply_markup=generate_menu())

def generate_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Подписаться на рассылку", "Показать расписание")
    keyboard.row("Помощь")
    return keyboard

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS message (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()

def insert_or_update_user(chat_id, group_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO message (id, name) VALUES (?, ?)", (chat_id, group_name))
    conn.commit()
    conn.close()

def send_schedule_notification(user_id, group_name, schedule_data):
    schedule_for_today = []
    for row in schedule_data:
        schedule_date = datetime.strptime(row[1], '%d-%m-%Y').date()
        if schedule_date == date.today():
            schedule_for_today.append(row)

    if schedule_for_today:
        schedule_text = f"Привет! Твое расписание для группы '{group_name}' на сегодня:\n"
        for row in schedule_for_today:
            if row[5] == group_name:
                schedule_text += f"День: {row[1]}\nВремя: {row[2]}\nПредмет: {row[3]}\nОписание: {row[4]}\nГруппа: {row[5]}\nПреподаватель: {row[6]}\nСсылка: {row[7]}\n\n"
        bot.send_message(user_id, schedule_text)
    else:
        bot.send_message(user_id, f"На сегодня расписание для группы '{group_name}' отсутствует. 🤔")

# def check_new_subscriptions():
#     conn = sqlite3.connect(DATABASE_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, name FROM message")
#     users = cursor.fetchall()
#     conn.close()
#
#     today = date.today()
#
#     schedule_data = get_schedule_scheduleDb(today)
#
#     for user_id, group_name in users:
#         send_schedule_notification(user_id, group_name, schedule_data)
#
#     threading.Timer(300, check_new_subscriptions).start()
#
# check_new_subscriptions()

bot.polling()


# Запускаем функцию рассылки
if __name__ == "__main__":
    generate_menu()
    bot.polling()