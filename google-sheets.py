from google.oauth2.service_account import Credentials
import gspread
from main import schedule, table_name
from datetime import datetime, timedelta, date
import re

sheet_id = "1MRXzlw20uGOOkX-0zNXOS9zuWvuORoSVk5ouAq05Tls"


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


process_sheets(sheet_id)


