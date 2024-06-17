#не работает
from main import bot, DATABASE_NAME, get_schedule_scheduleDb, generate_menu
from datetime import datetime, date
import sqlite3

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