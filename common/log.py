import os
import sys
import logging.config
import yaml
from functools import wraps
from copy import deepcopy


class SelfError(BaseException):
    '''自定义异常类'''
    def __init__(self, error_msg):
        super().__init__(self)
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class LogRecord(object):

    def __init__(self):
        self.logger = logging.getLogger()
        with open(file='../conflog.yaml', mode='r', encoding='utf-8') as f:
            self.conf = yaml.load(f.read(), Loader=yaml.FullLoader)

    def _file_address(self):
        config = deepcopy(self.conf)
        del config['handlers']['warning']
        del config['handlers']['error']
        config['loggers']['simpleExample']['handlers'].pop(1)
        config['loggers']['simpleExample']['handlers'].pop(1)
        config['root']['handlers'].pop(1)
        config['root']['handlers'].pop(1)
        logging.config.dictConfig(config)

    def _file_address_warn(self):
        log_path1 = (os.path.join(os.getcwd(), 'Log/DebugLog/'))
        os.makedirs(log_path1, exist_ok=True)
        config = deepcopy(self.conf)
        del config['handlers']['error']
        config['loggers']['simpleExample']['handlers'].pop(2)
        config['root']['handlers'].pop(2)
        logging.config.dictConfig(config)

    def _file_address_error(self):
        log_path2 = (os.path.join(os.getcwd(), 'Log/ErrorLog/'))
        os.makedirs(log_path2, exist_ok=True)
        config = deepcopy(self.conf)
        del config['handlers']['warning']
        config['loggers']['simpleExample']['handlers'].pop(1)
        config['root']['handlers'].pop(1)
        logging.config.dictConfig(config)

    def write_into_log(self, msg, level='debug'):
        if level == 'debug':
            if len(self.conf['handlers']) != 1:
                self._file_address()
            self.logger.debug(msg)
        elif level == 'info':
            if 'error' in self.conf['handlers']:
                self._file_address_warn()
            self.logger.info(msg)
        elif level == 'warning':
            if 'error' in self.conf['handlers']:
                self._file_address_warn()
            self.logger.warning(msg)
        elif level == 'error':
            if 'warning' in self.conf['handlers']:
                self._file_address_error()
            self.logger.error(msg)
        elif level == 'critical':
            if 'warning' in self.conf['handlers']:
                self._file_address_error()
            self.logger.critical(msg)
        else:
            raise SelfError('level参数错误：%s' % level)


class LogManage(LogRecord):

    def __init__(self, level=0):
        super().__init__()
        self._level = level

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._level > 3 or self._level < 0:
                self._file_address_warn()
                self.logger.warning('level参数错误：%s' % self._level)
                raise SelfError('level参数错误：%s' % self._level)
            result = func(*args, **kwargs)
            res = '{} - Flie: {}'.format(result, sys.argv[0])
            if issubclass(type(result), Exception):
                if 'warning' in self.conf['handlers']:
                    self._file_address_error()
                try:
                    raise result
                except Exception:
                    self.logger.exception('There is an anomaly happening in method：%s - File: %s ' % (func.__name__, sys.argv[0]))
            elif self._level == 0 and result:
                if len(self.conf['handlers']) != 1:
                    self._file_address()
                self.logger.debug(res)
            elif self._level == 1 and result:
                if len(self.conf['handlers']) != 1:
                    self._file_address()
                self.logger.debug(res)
            elif self._level == 2 and result:
                if 'error' in self.conf['handlers']:
                    self._file_address_warn()
                self.logger.info(res)
            elif self._level == 3 and result:
                if 'error' in self.conf['handlers']:
                    self._file_address_warn()
                self.logger.warning(res)
            return result
        return wrapper
