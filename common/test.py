def data(data, isrow=True):
    if isinstance(data, list):
        if not isinstance(data[0], list):
            if isrow is True:
                print(data)  # 行
        else:
            print(data)
    else:
        raise TypeError('The argument must be a list')


data([[1, 2], 1])
# data([5, 9])