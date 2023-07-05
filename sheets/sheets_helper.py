import gspread
from datetime import datetime


def add_expense(amount):
    # sa = gspread.service_account(filename="../service_account.json")
    sa = gspread.service_account(filename="/etc/secrets/service_account.json")
    spreadsheet = sa.open("Accounting")
    working_spread_sheet = spreadsheet.worksheet("Spenses")

    date = datetime.now().date()
    date = date.strftime('%m/%d/%Y')

    data = ("amount", date)

    working_spread_sheet.append_row(data)
