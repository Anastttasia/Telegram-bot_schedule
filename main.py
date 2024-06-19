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
    conn.close()
    return schedule_data

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! 👋 Я бот, который может отправлять тебе расписание.", reply_markup=generate_initial_menu())

@bot.message_handler(func=lambda message: message.text == "Указать номер группы")
def subscribe_handler(message):
    bot.send_message(message.chat.id, "Пожалуйста, укажите номер вашей группы.", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, handle_group_response)
@bot.message_handler(func=lambda message: message.text == "Изменить номер группы")
def change_group_handler(message):
    bot.send_message(message.chat.id, "Пожалуйста, укажите новый номер вашей группы.", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, handle_group_response)

def handle_group_response(msg):
    user_id = msg.chat.id
    group_name = msg.text
    if not group_name.isdigit() or len(group_name) > 2:
        bot.send_message(user_id, "Ошибка: Пожалуйста, введите корректный номер группы (не более 2 чисел).", reply_markup=generate_initial_menu())
        return

    insert_or_update_user(user_id, group_name)
    bot.send_message(user_id, "Вы успешно указали номер группы! 🎉", reply_markup=generate_main_menu())

@bot.message_handler(func=lambda message: message.text == "Показать расписание")
def show_schedule_handler(message):
    conn_message = sqlite3.connect(DATABASE_NAME)
    cursor_message = conn_message.cursor()
    cursor_message.execute("SELECT name FROM message WHERE id = ?", (message.chat.id,))
    result = cursor_message.fetchone()
    if not result:
        bot.send_message(message.chat.id, "Сначала укажите номер группы.", reply_markup=generate_initial_menu())
        return

    group_name = result[0]
    today = date.today()
    schedule_data = get_schedule_scheduleDb(today, group_name)

    if schedule_data:
        schedule_text = f"Привет, твое расписание на сегодня для группы {group_name}:\n"
        for row in schedule_data:
            schedule_text += f"День: {row[1]}\nВремя: {row[2]}\nПредмет: {row[3]}\nОписание: {row[4]}\nГруппа: {row[5]}\nПреподаватель: {row[6]}\nСсылка: {row[7]}\n\n"
        m = schedule_text
        if len(m) > 4095:
            for x in range(0, len(m), 4095):
                bot.send_message(message.chat.id, text=m[x:x + 4095])
        else:
            bot.send_message(message.chat.id, text=m)
    else:
        bot.send_message(message.chat.id, "На сегодня расписание отсутствует. 🤔", reply_markup=generate_main_menu())

@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_handler(message):
    bot.send_message(message.chat.id, "Я могу отправлять вам расписание каждый день в 9:00 утра.\n\nВы можете указать номер группы, чтобы получать расписание, или просто посмотреть его прямо сейчас.\n\nИспользуйте кнопки ниже для взаимодействия со мной.", reply_markup=generate_main_menu())

@bot.message_handler(func=lambda message: message.text == "Отписаться от рассылки")
def unsubscribe_handler(message):
    user_id = message.chat.id
    delete_user(user_id)
    bot.send_message(user_id, "Вы успешно отписались от рассылки. 😢", reply_markup=generate_initial_menu())

def generate_initial_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Указать номер группы")
    return keyboard

def generate_main_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Показать расписание")
    keyboard.row("Изменить номер группы", "Отписаться от рассылки")
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
def delete_user(chat_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM message WHERE id = ?", (chat_id,))
    conn.commit()
    conn.close()

def insert_or_update_user(chat_id, group_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO message (id, name) VALUES (?, ?)", (chat_id, group_name))
    conn.commit()
    conn.close()

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
    bot.polling()