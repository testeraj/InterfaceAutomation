import pytest
from filelock import FileLock
from common.mysqldb import Mysql
from common.request import Request
from common.excel import readonly
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
    data = readonly(PATH)
    response = request.initiate(method=data[0][3], url=IP+data[0][4], data=data[0][5])
    token = response.json()['data']['token']
    return '{"token": "%s"}' % token

