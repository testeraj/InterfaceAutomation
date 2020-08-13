def data(data, isrow=True):
    print(len(data))
    print(([le for le in list(map(lambda x: len(x), [row for row in data])) if len(data[0]) == le]))
    if len(data) != len([le for le in list(map(lambda x: len(x), [row for row in data])) if le == len(data[0])]):
        print(1)



data([[1, 2, 3], [1, 6]])
# data([5, 9])