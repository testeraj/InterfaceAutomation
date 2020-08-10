import os
import sys
import logging.config
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

    def __init__(self, config):
        self.logger = logging.getLogger()
        self.config = config

    def _file_address(self):
        config = deepcopy(self.config)
        del config['handlers']['warning']
        del config['handlers']['error']
        config['loggers']['simpleExample']['handlers'].pop(1)
        config['loggers']['simpleExample']['handlers'].pop(1)
        config['root']['handlers'].pop(1)
        config['root']['handlers'].pop(1)
        logging.config.dictConfig(config)

    def _file_address_warn(self):
        log_path1 = (os.path.join(os.getcwd(), 'Logs/DebugLogs/'))
        os.makedirs(log_path1, exist_ok=True)
        config = deepcopy(self.config)
        del config['handlers']['error']
        config['loggers']['simpleExample']['handlers'].pop(2)
        config['root']['handlers'].pop(2)
        logging.config.dictConfig(config)

    def _file_address_error(self):
        log_path2 = (os.path.join(os.getcwd(), 'Logs/ErrorLogs/'))
        os.makedirs(log_path2, exist_ok=True)
        config = deepcopy(self.config)
        del config['handlers']['warning']
        config['loggers']['simpleExample']['handlers'].pop(1)
        config['root']['handlers'].pop(1)
        logging.config.dictConfig(config)

    def write_into_log(self, msg, level='debug'):
        if level == 'debug':
            if len(self.config['handlers']) != 1:
                self._file_address()
            self.logger.debug(msg)
        elif level == 'info':
            if 'error' in self.config['handlers']:
                self._file_address_warn()
            self.logger.info(msg)
        elif level == 'warning':
            if 'error' in self.config['handlers']:
                self._file_address_warn()
            self.logger.warning(msg)
        elif level == 'error':
            if 'warning' in self.config['handlers']:
                self._file_address_error()
            self.logger.error(msg)
        elif level == 'critical':
            if 'warning' in self.config['handlers']:
                self._file_address_error()
            self.logger.critical(msg)
        else:
            raise SelfError('level参数错误：%s' % level)


class LogManage(LogRecord):

    def __init__(self, config, level=0):
        super().__init__(config=config)
        self._level = level
        self.logger = logging.getLogger()
        self.config = config

    def __call__(self, func):
        '''
        用于记录日志的装饰器，此装饰器可以将函数的返回值记录下来
            @LogManage(level=0)
            def log()
                try:
                    pass
                except BaseException as e:
                    return e
        :param level: 日志输出的级别
        :return:
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._level > 3 or self._level < 0:
                self._file_address_warn()
                self.logger.warning('level参数错误：%s' % self._level)
                raise SelfError('level参数错误：%s' % self._level)
            result = func(*args, **kwargs)
            res = '{} - Flie: {}'.format(result, sys.argv[0])
            if issubclass(type(result), Exception):
                if 'warning' in self.config['handlers']:
                    self._file_address_error()
                try:
                    raise result
                except Exception:
                    self.logger.exception('There is an anomaly happening in method：%s - File: %s ' % (func.__name__, sys.argv[0]))
            elif self._level == 1 and result:
                if len(self.config['handlers']) != 1:
                    self._file_address()
                self.logger.debug(res)
            elif self._level == 2 and result:
                if 'error' in self.config['handlers']:
                    self._file_address_warn()
                self.logger.info(res)
            elif self._level == 3 and result:
                if 'error' in self.config['handlers']:
                    self._file_address_warn()
                self.logger.warning(res)
            return result
        return wrapper
