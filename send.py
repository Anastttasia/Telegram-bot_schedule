#не работает
import sqlite3
from datetime import date, datetime
import telebot
from telebot import types
import time

BOT_TOKEN = '6324418773:AAEIWge54hrrxGvRnJepfgLC4y7u_A7Me_A'
USERS_DATABASE = 'message.db'
SCHEDULE_DATABASE = 'schedule.db'
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для получения расписания из базы данных
def get_schedule_scheduleDb(date, group_name):
    conn = sqlite3.connect(SCHEDULE_DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM schedule WHERE schedule_date = ? AND group_name = ?",
        (date.strftime('%d-%m-%Y'), group_name))
    schedule_data = cursor.fetchall()
    conn.close()
    return schedule_data


# Функция для отправки расписания пользователям
def send_schedule_to_users():
    # Подключение к базе данных с пользователями
    conn_users = sqlite3.connect(USERS_DATABASE)
    cursor_users = conn_users.cursor()

    # Получаем всех пользователей
    cursor_users.execute(
        "SELECT id, name FROM message")
    users = cursor_users.fetchall()
    conn_users.close()

    # Подключение к базе данных с расписанием
    conn_schedule = sqlite3.connect(SCHEDULE_DATABASE)
    cursor_schedule = conn_schedule.cursor()

    # Получаем расписание на сегодня для всех групп
    today = date.today().strftime('%d-%m-%Y')
    cursor_schedule.execute("SELECT * FROM schedule WHERE schedule_date = ?",
                           (today,))
    schedule_data = cursor_schedule.fetchall()

    # Группируем расписание по группам
    schedule_by_group = {}
    for row in schedule_data:
        group_name = row[5]
        if group_name not in schedule_by_group:
            schedule_by_group[group_name] = []
        schedule_by_group[group_name].append(row)

    # Проходим по пользователям и отправляем расписание
    for user_id, group_name in users:
        user_schedule = schedule_by_group.get(group_name)
        if user_schedule:
            schedule_text = f"Привет, {group_name}, твое расписание на сегодня:\n"
            for row in user_schedule:
                schedule_text += f"Время: {row[2]}\nПредмет: {row[3]}\nОписание: {row[4]}\nПреподаватель: {row[6]}\nСсылка: {row[7]}\n\n"

            # Отправляем сообщение с учетом ограничения длины
            if len(schedule_text) > 4095:
                for x in range(0, len(schedule_text), 4095):
                    bot.send_message(user_id, text=schedule_text[x:x + 4095])
            else:
                bot.send_message(user_id, text=schedule_text)
        else:
            bot.send_message(user_id, "На сегодня расписание отсутствует. 🤔")
    conn_schedule.close()

bot.polling(none_stop=True)