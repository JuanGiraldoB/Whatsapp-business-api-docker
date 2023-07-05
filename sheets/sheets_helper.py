import gspread
from datetime import datetime


def add_expense(amount):
    # sa = gspread.service_account(filename="../service_account.json")
    sa = gspread.service_account(filename="/etc/secrets/service_account.json")
    spreadsheet = sa.open("Accounting")
    working_spread_sheet = spreadsheet.worksheet("Spenses")

    date = datetime.now().date()
    date = date.strftime('%m/%d/%Y')

    data = (amount, date)

    working_spread_sheet.append_row(data)


def get_total_expenses():
    # sa = gspread.service_account(filename="../service_account.json")
    sa = gspread.service_account(filename="/etc/secrets/service_account.json")
    spreadsheet = sa.open("Accounting")
    working_spread_sheet = spreadsheet.worksheet("Spenses")

    all_records = working_spread_sheet.get_all_records()

    total_amount = sum(row['Amount'] for row in all_records)

    return total_amount
