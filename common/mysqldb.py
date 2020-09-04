import pymysql
from common.log import LogRecord


class Mysql(object):

    def __init__(self, config):
        self.config = config['database']
        self._mysqldb = pymysql.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['dbname'],
            port=self.config['port'],
            charset=self.config['charset'],
        )
        self._mycursor = self._mysqldb.cursor()

    def execute_sql(self, sql, fetch=0):
        try:
            self._mysqldb.ping(reconnect=True)
            if sql[:6] in ('update', 'insert', 'delete'):
                self._mycursor.execute(sql)
                LogRecord().write_into_log(self._mycursor.mogrify(sql))
                self._mysqldb.commit()  # 提交修改
            elif sql[:6] == "select":
                self._mycursor.execute(sql)
                if fetch == 0:
                    result = self._mycursor.fetchone()
                    LogRecord().write_into_log("{} ---> {}".format(result, self._mycursor.mogrify(sql)))
                    self._mysqldb.commit()
                    return result
                elif fetch == 1:
                    result = self._mycursor.fetchall()
                    LogRecord().write_into_log("{} ---> {}".format(result, self._mycursor.mogrify(sql)))
                    self._mysqldb.commit()
                    return result
                else:
                    raise TypeError('Parameter Error')
            else:
                raise TypeError('Parameter Error')
        except BaseException as e:
            self._mysqldb.rollback()    # 发生错误时回滚
            LogRecord().write_into_log(e, level=3)

    def close(self):
        self._mycursor.close()   # 关闭游标
        self._mysqldb.close()     # 关闭连接
