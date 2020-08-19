import requests
from functools import wraps


class Request:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs.setdefault('file')
        self.kwargs.setdefault('params')
        self.kwargs.setdefault('data')
        self.kwargs.setdefault('json')
        self.kwargs.setdefault('headers')

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = requests.request(
                method=self.kwargs['method'],
                url=self.kwargs['url'],
                json=self.kwargs['json'],
                headers=self.kwargs['headers'])
            result = func(response, *args, **kwargs)
            return result
        return wrapper


@Request(method='post', url='http://www.httpbin.org/post')
def airtest(*args, **kwargs):
    print(*args)
    print('1111')

airtest(123)