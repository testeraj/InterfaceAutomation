import requests
from common.encryption import Encryption


def start(options=None, **kwargs):
    if kwargs.get('method') is not None or kwargs.get('url') is not None:
        kwargs.setdefault('json')
        kwargs.setdefault('data')
        kwargs.setdefault('params')
        kwargs.setdefault('file')
        kwargs.setdefault('headers')
        for k, v in kwargs.items():
            if v is not None and v != '':
                if v[0] == '{' and v[-1] == '}':
                    kwargs[k] = eval(v)
                else:
                    kwargs[k] = v

        if len(list(filter(lambda x: x is not None and x != '', [kwargs['json'], kwargs['data'], kwargs['params']]))) == 1:
            if options == 'md5' or options == 'base64':
                res = eval(list(filter(lambda x: x is not None and x != '', [kwargs['json'], kwargs['data']]))[0])
                for k, v in res.items():
                    if v == "" or v is None:
                        res[k] = v
                    else:
                        encrypted_data = getattr(Encryption, options)(v)
                        res[k] = encrypted_data
                if kwargs['json'] is None:
                    kwargs['data'] = res
                elif kwargs['data'] is None:
                    kwargs['json'] = res
                response = requests.request(
                    method=kwargs['method'],
                    url=kwargs['url'],
                    json=json,
                    data=data,
                    params=kwargs.setdefault('params'),
                    files=kwargs.setdefault('file'),
                    headers=kwargs.setdefault('headers'))
                return response
            elif options is None:
                response = requests.request(
                    method=kwargs['method'],
                    url=kwargs['url'],
                    json=json,
                    data=data,
                    params=kwargs.setdefault('params'),
                    files=kwargs.setdefault('file'),
                    headers=kwargs.setdefault('headers'))
                return response
            else:
                raise ValueError('only md5 or base64 can be passed in')
        else:
            raise ValueError('only one data type can be passed')
    else:
        raise KeyError('Missing the necessary parameters')

    # elif len(list(filter(lambda x: x is not None and x != '', [kwargs.setdefault('json'), kwargs.setdefault('data'), kwargs.setdefault('params')]))) == 1:
    #     raise ValueError('only one data type can be passed')
    # if options == 'md5' or options == 'base64':
    #     res = eval(list(filter(lambda x: x is not None and x != '', [kwargs['json'], kwargs['data']]))[0])
    #     for k, v in res.items():
    #         if v == "" or v is None:
    #             res[k] = v
    #         else:
    #             encrypted_data = getattr(Encryption, options)(v)
    #             res[k] = encrypted_data
    #     if kwargs['json'] is None:
    #         kwargs['data'] = res
    #     elif kwargs['data'] is None:
    #         kwargs['json'] = res
    #     print(kwargs['json'])
    #     print(kwargs['data'])
    #     response = requests.request(
    #         method=kwargs['method'],
    #         url=kwargs['url'],
    #         json=kwargs['json'],
    #         data=kwargs['data'],
    #         params=kwargs.setdefault('params'),
    #         files=kwargs.setdefault('file'),
    #         headers=kwargs.setdefault('headers'))
    #     return response
    # elif options is None:
    #     if kwargs.setdefault('json') is not None:
    #         json = eval(kwargs['json'])
    #     elif kwargs.setdefault('data') is not None:
    #         data = eval(kwargs['data'])
    #     response = requests.request(
    #         method=kwargs['method'],
    #         url=kwargs['url'],
    #         json=json,
    #         data=data,
    #         params=kwargs.setdefault('params'),
    #         files=kwargs.setdefault('file'),
    #         headers=kwargs.setdefault('headers'))
    #     return response
    # else:
    #     raise ValueError('only md5 or base64 can be passed in')


result = start(method='post', url='http://192.168.1.46:1004/into/carEnterParkLotFree',
               data='{"carId": "京N8P8F8", "parkLotId": "648882264796561401"}'
              )


# print(result)
# print(result.text)