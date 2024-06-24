
import telebot
import sqlite3
from datetime import date
from db.schedule_db import ScheduleDB

# Константы
table_name = "Netology"
schedule = ScheduleDB()
schedule.createNewGroup(table_name)

BOT_TOKEN = '6324418773:AAFReFGni232-0CACfsQvNPdwEs5YM58nuo'

MAX_MESSAGE_LENGTH = 4095

DATABASE_NAME = "message.db"
DATABASE_SCHEDULE = "schedule.db"

MAX_MESSAGE_LENGTH = 4095

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)


# Функция для отправки расписания пользователям
def send_schedule_to_users():
    # Подключение к базе данных с пользователями
    conn_users = sqlite3.connect(DATABASE_NAME)
    cursor_users = conn_users.cursor()

    # Получаем всех пользователей
    cursor_users.execute("SELECT id, name FROM message")
    users = cursor_users.fetchall()
    conn_users.close()

    # Подключение к базе данных с расписанием
    conn_schedule = sqlite3.connect(DATABASE_SCHEDULE)
    cursor_schedule = conn_schedule.cursor()

    # Получаем расписание на сегодня для всех групп
    today = date.today().strftime('%d-%m-%Y')
    cursor_schedule.execute("SELECT * FROM Netology WHERE date = ?", (today,))
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
        user_schedule = schedule_by_group.get(int(group_name))

        if user_schedule:
            schedule_text = f"Привет, твое расписание на сегодня для группы {group_name}:\n"
            for row in user_schedule:
                schedule_text += (
                    f"День: {row[1]}\n"
                    f"Время: {row[2]}\n"
                    f"Предмет: {row[3]}\n"
                    f"Описание: {row[4]}\n"
                    f"Группа: {row[5]}\n"
                    f"Преподаватель: {row[6]}\n"
                    f"Ссылка: {row[7]}\n\n"
                )

            # Отправляем сообщение с учетом ограничения длины
            if len(schedule_text) > MAX_MESSAGE_LENGTH:
                for x in range(0, len(schedule_text), MAX_MESSAGE_LENGTH):
                    bot.send_message(user_id, text=schedule_text[x:x + MAX_MESSAGE_LENGTH])
            else:
                bot.send_message(user_id, text=schedule_text)
        else:
            bot.send_message(user_id, "На сегодня расписание отсутствует. 🤔")
    conn_schedule.close()


# Основная логика программы
send_schedule_to_users()
