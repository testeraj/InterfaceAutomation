import pymysql
from common.log import LogRecord


class Mysql(object):

    def __init__(self, config):
        self._mysqldb = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            port=config['port'],
            charset=config['charset'],
        )
        self._mycursor = self._mysqldb.cursor()

    def select(self, sql, level=0):
        try:
            self._mysqldb.ping(reconnect=True)
            if 'select' in sql:
                self._mycursor.execute(sql)
                if level == 0:
                    result = self._mycursor.fetchone()
                    LogRecord().write_into_log("{} ---> {}".format(result, self._mycursor.mogrify(sql)))
                    self._mysqldb.commit()
                    return result
                elif level == 1:
                    result = self._mycursor.fetchall()
                    LogRecord().write_into_log("{} ---> {}".format(result, self._mycursor.mogrify(sql)))
                    self._mysqldb.commit()  # 提交修改
                    return result
            elif 'update' in sql:
                self._mycursor.execute(sql)
                LogRecord().write_into_log(self._mycursor.mogrify(sql))
                self._mysqldb.commit()  # 提交修改
        except BaseException as e:
            self._mysqldb.rollback()    # 发生错误时回滚
            LogRecord().write_into_log(e, level='error')

    def close(self):
        self._mycursor.close()   # 关闭游标
        self._mysqldb.close()     # 关闭连接
