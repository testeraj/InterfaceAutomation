import os
import sys
import logging.config
import yaml
import shutil
from functools import wraps
from datetime import datetime


class LogRecord(object):

    def __init__(self):
        self.logger = logging.getLogger()
        with open(file='F:/InterfaceAutomation/config.yaml', mode='r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.conf = config['Log']
        os.makedirs(os.path.join(os.getcwd(), 'Logs/'), exist_ok=True)

    def _clear(self):
        filename = self.conf['handlers']['attribute']['filename']
        historyfile = os.path.join(os.getcwd(), 'Logs/history')
        if os.path.exists(filename) and round(os.path.getsize(filename)/1024/1024) >= 100:
            os.makedirs(historyfile, exist_ok=True)
            shutil.move(filename, historyfile)
            os.rename(historyfile+'/log.log', historyfile+'/{}.log'.format(
                datetime.now().strftime('%Y-%m-%d')))
        logging.config.dictConfig(self.conf)

    def write_into_log(self, msg, level=0):
        self._clear()
        if level == 0:
            self.logger.debug(msg)
        elif level == 1:
            self.logger.info(msg)
        elif level == 2:
            self.logger.warning(msg)
        elif level == 3:
            self.logger.error(msg)
        elif level == 4:
            self.logger.critical(msg)
        else:
            raise TypeError('Parameter Error')


class LogManage(LogRecord):

    def __init__(self, level=1):
        super().__init__()
        self._level = level

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._level > 3 or self._level < 1:
                self.logger.warning('level参数错误：%s' % self._level)
                raise TypeError('Parameter Error')
            self._clear()
            result = func(*args, **kwargs)
            res = '{} - Flie: {}'.format(result, sys.argv[0])
            if issubclass(type(result), Exception):
                try:
                    raise result
                except Exception:
                    self.logger.exception('There is an anomaly happening in method：%s - File: %s ' % (func.__name__, sys.argv[0]))
            elif self._level == 1 and result:
                self.logger.debug(res)
            elif self._level == 2 and result:
                self.logger.info(res)
            elif self._level == 3 and result:
                self.logger.warning(res)
            return result
        return wrapper
