def data(data, isrow=True):
    a = all(isinstance(row, list) for row in data)
    b = (isinstance(row, list) for row in data)
    print(a)


data([[1, 2], 1])
# data([5, 9])