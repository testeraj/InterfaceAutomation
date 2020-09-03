import pytest
from filelock import FileLock
from common.mysqldb import Mysql
from common.request import Request
from common.excel import Excel
from common.log import LogRecord
from common.readconfig import MYSQL_CONFIG, PATH, IP


@pytest.fixture(scope='session', autouse=True)
def control():
    with FileLock("session.lock"):
        logger = LogRecord()
        mydb = Mysql(MYSQL_CONFIG)
        request = Request
    yield logger, mydb, request
    mydb.close()


@pytest.fixture(scope='module')
def login(control):
    logger, mydb, request = control
    excel = Excel(PATH)
    try:
        data = excel.readExcel()
        data.pop(0)
        response = request.initiate(method=data[0][3], url=IP+data[0][4], data=data[0][5])
        token = response.json()['data']['token']
        for i in range(3, excel.row+1):
            excel.writeExcel(['{"token": "%s"}' % token], isrow=False, start=f'G{i}')
        return token
    except Exception as e:
        logger.write_into_log(e, 3)
    finally:
        excel.close()

