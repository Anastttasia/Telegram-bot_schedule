import gspread
from google.oauth2.service_account import Credentials
from db.schedule_db import ScheduleDB
import telebot
import sqlite3
from datetime import datetime, timedelta, date
import time
import re

table_name = "Netology"
schedule = ScheduleDB()
schedule.createNewGroup(table_name)
schedule.clearData(table_name)
def authenticate_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = Credentials.from_service_account_file("mypython-414513-94cec7c6b257.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client


def read_sheet(client, sheet_id, sheet_name):
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_values()  # Получает весь лист целиком, игнорируя пустые строки и столбцы
    return data


def get_sheets(client, sheet_id):
    sheet = client.open_by_key(sheet_id)
    worksheets = sheet.worksheets()
    return worksheets


def fill_dates(schedule, start_date):
    current_date = datetime.strptime(start_date, "%d-%m-%Y")
    previous_date = current_date.strftime("%d-%m-%Y")

    for entry in schedule:
        if len(entry) > 0 and entry[0]:  # Если первая ячейка не пустая, это новый день
            current_date = current_date + timedelta(days=1)
            entry[0] = current_date.strftime("%d-%m-%Y")
            previous_date = entry[0]
        elif len(entry) > 0:  # Если первая ячейка пустая, используем предыдущую дату
            entry[0] = previous_date

    return schedule


def process_sheets(sheet_id):
    client = authenticate_sheets()
    worksheets = get_sheets(client, sheet_id)

    date_pattern = re.compile(r'\d{2}-\d{2}-\d{4}')
    monday_sheets = []

    for worksheet in worksheets:
        sheet_name = worksheet.title
        if date_pattern.match(sheet_name):
            sheet_date = datetime.strptime(sheet_name, '%d-%m-%Y')
            if sheet_date.weekday() == 0:  # Проверка на понедельник
                monday_sheets.append((sheet_date, sheet_name))

    monday_sheets.sort()

    for sheet_date, sheet_name in monday_sheets:
        data = read_sheet(client, sheet_id, sheet_name)
        if data:
            print(f"Data from sheet {sheet_name}:")
            filtered_data = [row for row in data[1:] if any(cell.strip() for cell in row)]  # Пропускаем первую строку

            start_date = sheet_name  # Используем название листа как стартовую дату
            filled_data = fill_dates(filtered_data, start_date)
            for row in filled_data:
                schedule.insertData(table_name, row[0], row[1], row[2], row[3], int(row[4]), row[5], row[6])

        '''if current_date.weekday() == 6:  #если текущая дата = воскресенью (6 - воскресенье)
            next_monday_date = current_date + timedelta(days=(7 - current_date.weekday())) #мы вычисляем сколько дней до следующего понедельника, 7 - номер текущей даты и определяем следующую дату понедельника
            if sheet_date == next_monday_date: #если дата листа равна дате понедельника то добавляем условие
                data = read_sheet(client, sheet_id, sheet_name)
                print(data)

                #переместить
                if data:
                    pass'''


'''scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]


creds = Credentials.from_service_account_file("mypython-414513-94cec7c6b257.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1MRXzlw20uGOOkX-0zNXOS9zuWvuORoSVk5ouAq05Tls" #ссылка на гугл таблицу
sheet = client.open_by_key(sheet_id)'''


'''print("Before exec")
print(schedule.getDataByDate(table_name, '15-04-2024'))'''
'''while True:
    values_list = sheet.sheet1.row_values(counter)
    if (values_list == []):
        break
    # self, tableName, date, timeLesson, subjectName, subgroupNumber, teacherName, linkLesson
    schedule.insertData(table_name, values_list[0], values_list[1], values_list[2], int(values_list[3]), values_list[4], values_list[5])
    #print(values_list)
    counter += 1'''

'''print("After exec")
print(schedule.getDataByDate(table_name, '15-04-2024'))'''

'''
# Токен вашего бота
BOT_TOKEN = "6324418773:AAGqLSzRvKJzSbO721xM2CS9O0TL1t5BrBc"

# Название базы данных
DATABASE_NAME = "message.db"
DATABASE_SCHEDULE = "schedule.db"

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для получения расписания из базы данных
def get_schedule_message():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM message")
    schedule_data = cursor.fetchall()
    conn.close()
    return schedule_data

def get_schedule_scheduleDb():
    conn = sqlite3.connect(DATABASE_SCHEDULE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Netology")
    schedule_data1 = cursor.fetchall()
    conn.close()
    return schedule_data1

# Функция для отправки расписания пользователям
def send_schedule_to_users(schedule_data,schedule_data1):
    message = f"Hello! Here is your schedule for today:\n"

    for row in schedule_data:
        id = row[0]
        try:
            bot.send_message(id, message)
            print(f"Расписание отправлено пользователю {id}")
        except telebot.apihelper.ApiException as e:
            print(f"Ошибка при отправке расписания пользователю {id}: {e}")

# Функция для запуска рассылки в определенное время
def schedule_task():
    while True:
        now = datetime.datetime.now()
        if now.hour == 12 and now.minute == 23:  # Измените время на нужное
            schedule_data = get_schedule_message()
            send_schedule_to_users(schedule_data)
            print("Расписание отправлено!")

        time.sleep(60)  # Проверяем каждые 60 секунд

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! 👋  Я бот, который может отправлять вам расписание.", reply_markup=generate_menu())

# Обработка команды /subscribe
@bot.message_handler(func=lambda message: message.text == "Подписаться на рассылку")
def subscribe_handler(message):
    bot.send_message(message.chat.id, "К какой группе вы относитесь?", reply_markup=telebot.types.ReplyKeyboardRemove())

    @bot.message_handler(func=lambda m: m.chat.id == message.chat.id)
    def handle_group_response(msg):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO message (id, name) VALUES (?, ?)", (msg.chat.id, msg.text))
        bot.send_message(msg.chat.id, "Вы успешно подписались на рассылку! 🎉", reply_markup=generate_menu())

@bot.message_handler(func=lambda message: message.text == "Подписаться на рассылку")
def subscribe_handler(message):
    # Задаем вопрос о группе
    bot.send_message(message.chat.id, "К какой группе вы относитесь?", reply_markup=telebot.types.ReplyKeyboardRemove())

    # Ожидаем ответа
    @bot.message_handler(func=lambda m: m.chat.id == message.chat.id)
    def handle_group_response(msg):
        # Сохраняем информацию в базу данных
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        id = msg.chat.id
        name = msg.text
        cursor.execute("INSERT INTO message (id, name) VALUES (?, ?)", (id, name))
        conn.commit()
        conn.close()

        # Отправляем сообщение об успешной подписке
        bot.send_message(msg.chat.id, "Вы успешно подписались на рассылку! 🎉", reply_markup=generate_menu())

# Обработка команды /show_schedule
@bot.message_handler(func=lambda message: message.text == "Показать расписание")
def show_schedule_handler(message):
    # Получаем текущую дату
    today = date.today()

    # Получаем расписание из базы данных
    schedule_data = get_schedule_scheduleDb()

    # Проверяем, есть ли записи в расписании для сегодняшней даты
    schedule_for_today = []
    for row in schedule_data:
        schedule_date = datetime.strptime(row[1], '%d-%m-%Y').date()
        if schedule_date == today:
            schedule_for_today.append(row)

    # Формируем сообщение
    if schedule_for_today:
        schedule_text = "Привет, твое расписание на сегодня:\n"
        for row in schedule_for_today:
            schedule_text += f"Date: {row[1]}\n"
            schedule_text += f"Time: {row[2]}\n"
            schedule_text += f"Subject: {row[3]}\n"
            schedule_text += f"Subgroup: {row[4]}\n"
            schedule_text += f"Teacher: {row[5]}\n"
            schedule_text += f"Link: {row[6]}\n\n"
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
    bot.send_message(message.chat.id, "Я могу отправлять вам расписание каждый день в 7:00 утра.\n\nВы можете подписаться на рассылку, чтобы получать расписание, или просто посмотреть его прямо сейчас.\n\nИспользуйте кнопки ниже для взаимодействия со мной.", reply_markup=generate_menu())

# Функция для создания меню с кнопками
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
'''

# Запускаем функцию рассылки
if __name__ == "__main__":
    #generate_menu()
    #bot.polling()
    sheet_id = "1MRXzlw20uGOOkX-0zNXOS9zuWvuORoSVk5ouAq05Tls"
    process_sheets(sheet_id)


