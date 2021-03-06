import os
import xlrd
import xlwings as xw


def readonly(file):
    if os.path.exists(file):
        workbook = xlrd.open_workbook(file)  # 打开execl表
        sheet = workbook.sheets()[0]  # 获取工作页w
        new_data = []
        for i in range(1, sheet.nrows):
            value = sheet.row_values(i)
            new_value = [None if v == '' else v for v in value]
            new_data.append(new_value)
        return new_data
    else:
        raise FileNotFoundError('file or path does not exist')


class Excel:

    def __init__(self, file, sheet_name='sheet1', visible=False):
        """
        :param file: 文件路径，如果文件不存在，则新建文件
        :param sheet_name: 工作页名称
        :param visible: bool, 该值决定是否打开应用程序(Excel) 默认False
        """
        self.__app = xw.App(visible=visible, add_book=False)
        self.__app.display_alerts = False
        self.__app.screen_updating = False
        if os.path.exists(file):
            self.workbook = self.__app.books.open(file)          # 打开已有文件
        else:
            self.workbook = self.__app.books.add()                   # 新建文件
        self.sheet = self.workbook.sheets[sheet_name]
        info = self.sheet.used_range
        self.column = info.last_cell.column  # 列数
        self.row = info.last_cell.row  # 行数

    def readExcel(self, start='A1'):
        data = self.sheet.range(start).expand().value
        return data

    def writeExcel(self, data, isrow=True, start='A1'):
        '''
        :param data: list, 参数必须为列表; 可以传嵌套列表  [args, args, args] or [[args, args], [args, args], [args, args]]
        :param isrow: bool, 区分行和列, 默认为True(行)
        :param start: str, Excel中的单元格
        '''
        if isinstance(data, list):
            if all(isinstance(row, (str, int)) for row in data):
                if isrow is True:
                    self.sheet.range(start).value = data  # 行
                elif isrow is False:
                    self.sheet.range(start).options(transpose=True).value = data  # 列
                    # self.sheet.range(start).value = [[1], [2], [3], [4]]                    # 列
                else:
                    raise TypeError('The parameter must be a Boolean value')
            elif all(isinstance(row, list) for row in data):
                if len(data) <= 1:
                    raise TypeError('The length of a 2d list should be greater than 1')
                if len(data) != \
                        len([le for le in list(map(lambda x: len(x), [row for row in data])) if len(data[0]) == le]):
                    raise TypeError('All elements of a 2d list must be of the same length')
                else:
                    self.sheet.range(start).value = data
            else:
                raise TypeError('All elements of a 2d list must be list')
        else:
            raise TypeError('The argument must be a list')

    def close(self):
        self.workbook.save()
        self.workbook.close()
        self.__app.quit()
