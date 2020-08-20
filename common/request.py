import requests
from functools import wraps


class Request:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if self.kwargs.get('method') is None or self.kwargs.get('url') is None:
            raise KeyError('Missing the necessary parameters')
        self.kwargs.setdefault('json')
        self.kwargs.setdefault('data')
        self.kwargs.setdefault('params')
        self.kwargs.setdefault('file')
        self.kwargs.setdefault('headers')

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = requests.request(
                method=self.kwargs['method'],
                url=self.kwargs['url'],
                json=self.kwargs['json'],
                data=self.kwargs['data'],
                params=self.kwargs['params'],
                files=self.kwargs['file'],
                headers=self.kwargs['headers'])
            result = func(response, *args, **kwargs)
            return result
        return wrapper
