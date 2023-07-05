import gspread

sa = gspread.service_account(filename="service_account.json")
sh = sa.open("Accounting")

wks = sh.worksheet("Deudas")

# print("Rows: ", wks.row_count)
# print("Cols: ", wks.col_count)

# print(wks.acell('A2').value)
# print(wks.get("A1:D5"))

# print(wks.get_all_records())
# print(wks.get_all_values())

wks.update('A22', 'hola')
