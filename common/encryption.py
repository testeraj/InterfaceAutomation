import base64
import hashlib


class Encryption(object):

    @staticmethod
    def md5(data: str):
        if isinstance(data, str):
            md5 = hashlib.md5()
            md5.update(data.encode('utf-8'))
            return md5.hexdigest()
        else:
            raise TypeError('Parameter type error')

    @staticmethod
    def base64(data: str):
        if isinstance(data, str):
            return str(base64.b64encode(data.encode('utf-8')), 'utf-8')
        else:
            raise TypeError('Parameter type error')


if __name__ == '__main__':
    start = Encryption()
