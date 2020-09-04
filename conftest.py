import pytest
from filelock import FileLock
from common.mysqldb import Mysql
from common.request import Request
from common.log import LogRecord
from common.readdata import MYSQL_CONFIG, LOGIN, IP


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
    response = request.initiate(method=LOGIN[0][3], url=IP+LOGIN[0][4], data=LOGIN[0][5])
    token = response.json()['data']['token']
    return '{"token": "%s"}' % token
