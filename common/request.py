import requests
from common.encryption import Encryption


class Request:

    @staticmethod
    def __dispose(options, **kwargs):
        if kwargs.get('method') is not None and kwargs.get('url') is not None:
            kwargs.setdefault('json')
            kwargs.setdefault('data')
            kwargs.setdefault('params')
            kwargs.setdefault('file')
            kwargs.setdefault('headers')
            if len(list(filter(lambda x: x is not None and x != '', [kwargs['json'], kwargs['data'], kwargs['params']]))) == 1:
                if options is None:
                    for k, v in kwargs.items():
                        if v is not None and v != '':
                            if v[0] == '{' and v[-1] == '}':
                                kwargs[k] = eval(v)
                            else:
                                kwargs[k] = v
                    return kwargs
                elif options == 'md5' or options == 'base64':
                    for k, v in kwargs.items():
                        if v is not None and v != '':
                            if v[0] == '{' and v[-1] == '}':
                                kwargs[k] = eval(v)
                                if kwargs['json'] is not None:
                                    for key, value in kwargs['json'].items():
                                        if value == "" or value is None:
                                            kwargs['json'][key] = value
                                        else:
                                            encrypted_data = getattr(Encryption, options)(value)
                                            kwargs['json'][key] = encrypted_data
                                    return kwargs
                                elif kwargs['data'] is not None:
                                    for key, value in kwargs['data'].items():
                                        if value == "" or value is None:
                                            kwargs['data'][key] = value
                                        else:
                                            encrypted_data = getattr(Encryption, options)(value)
                                            kwargs['data'][key] = encrypted_data
                                    return kwargs
                                else:
                                    return kwargs
                            else:
                                kwargs[k] = v
                    return kwargs
                else:
                    raise ValueError('Only md5 or base64 can be passed in')
            else:
                raise ValueError('There can only be one value')
        else:
            raise KeyError('Missing the necessary parameters')

    @staticmethod
    def initiate(options=None, **kwargs):
        value = Request.__dispose(options, **kwargs)
        response = requests.request(
            method=value['method'],
            url=value['url'],
            json=value['json'],
            data=value['data'],
            params=value['params'],
            files=value['file'],
            headers=value['headers'])
        return response
