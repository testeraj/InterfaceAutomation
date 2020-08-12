import xlwings as xw


class OpenExecl:

    def __init__(self, file=None, sheet_name='sheet1', visible=False):
        """
        :param file: 文件路径，如果文件不存在，则新建文件
        :param sheet_name: 工作页名称
        :param visible: bool, 该值决定是否打开应用程序(execl) 默认False
        """
        self.__app = xw.App(visible=visible, add_book=False)
        self.__app.display_alerts = False
        self.__app.screen_updating = False
        if file:
            self.workbook = self.__app.books.open(file)          # 打开已有文件
        else:
            self.workbook = self.__app.books.add()                   # 新建文件
        self.sheet = self.workbook.sheets[sheet_name]
        info = self.sheet.used_range
        self.row = info.last_cell.column  # 列数
        self.nrows = info.last_cell.row  # 行数

    def readexecl(self, start='A1'):
        data = self.sheet.range(start).expand().value
        return data

    def writeexecl(self, data, start='A1'):
        self.sheet.range(start).value = [[1, 'AJ', 3], [2, 'KB', 10], [3, 'h', 51], [4, 9, 00]]    # 一个二维列表对应一行
        self.sheet.range(start).value = [[1], [2], [3], [4]]    # 对列
        self.sheet.range(start).value = [1, 2, 3, 4]     # 对行

    def close(self):
        self.workbook.save()
        self.workbook.close()
        self.__app.quit()
