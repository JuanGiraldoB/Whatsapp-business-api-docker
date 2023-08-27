import gspread
from datetime import datetime


class ExpenseManager:
    def __init__(self, service_account_path, spread_sheet, worksheet):
        self.sa = gspread.service_account(filename=service_account_path)
        self.spreadsheet = self.sa.open(spread_sheet)
        self.worksheet = self.spreadsheet.worksheet(worksheet)

    def add_expense(self, amount):
        date = datetime.now().date().strftime('%m/%d/%Y')
        data = (amount, date)
        self.worksheet.append_row(data)

    def get_total_expenses(self):
        all_records = self.worksheet.get_all_records()
        total_amount = sum(row['Amount'] for row in all_records)
        return total_amount

    def delete_expenses(self):
        values = self.worksheet.get_all_values()
        header_row = values[0]
        empty_values = [["" for _ in header_row] for _ in values[1:]]

        # Update the worksheet with empty values, starting from the second row
        self.worksheet.update("A2", empty_values)


if __name__ == "__main__":
    service_account_filename = "../service_account.json"
    expense_manager = ExpenseManager(
        service_account_filename, "Accounting", "Spenses")
    expense_manager.add_expense(10500)
    total_expenses = expense_manager.get_total_expenses()
    expense_manager.delete_expenses()
