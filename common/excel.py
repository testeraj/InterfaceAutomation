import xlwings as xw

app = xw.App(visible=True, add_book=False)
# app.display_alerts = False
# app.screen_updating = False
wb = app.books.open('test.xlsx')   # 打开已有文件
sht = wb.sheets['sheet1']
# sht.range('A1').value = [[1], [2], [3]]
a = sht.range('A1').expand().value
print(a)
info = sht.used_range
row = info.last_cell.column  # 列数
nrows = info.last_cell.row   # 行数
print(nrows, row)
wb.save()
wb.close()
app.quit()

# wb = app.books.add()    # 新建文件
# wb.save(r'test.xlsx')
# wb.close()
# app.quit()

