import xlwings as xw


class Execl:

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
        self.column = info.last_cell.column  # 列数
        self.row = info.last_cell.row  # 行数

    def readexecl(self, start='A1'):
        data = self.sheet.range(start).expand().value
        return data

    def writeexecl(self, data, isrow=True, start='A1'):
        '''
        :param data: list, 参数必须为列表; 可以传嵌套列表  [args, args, args] or [[args, args], [args, args], [args, args]]
        :param isrow: bool, 区分行和列, 默认为True(行)
        :param start: str, execl中的单元格
        '''
        if isinstance(data, list):
            result = [arg for arg in data]
            if not isinstance(result[0], list):
                if isrow is True:
                    self.sheet.range(start).value = result     # 行
                elif isrow is False:
                    self.sheet.range(start).options(transpose=True).value = result     # 列
                    # self.sheet.range(start).value = [[1], [2], [3], [4]]                    # 列
                else:
                    raise TypeError('The parameter must be a Boolean value')
            else:
                self.sheet.range(start).value = result
        else:
            raise TypeError('The argument must be a list')

    def close(self):
        self.workbook.save()
        self.workbook.close()
        self.__app.quit()
