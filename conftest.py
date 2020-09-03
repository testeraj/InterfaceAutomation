import pytest
from filelock import FileLock
from common.excel import readonly
from common.mysqldb import Mysql
from common.request import Request
from common.readconfig import MYSQL_CONFIG, PATH


@pytest.fixture(scope='session', autouse=True)
def control():
    with FileLock("session.lock"):
        mydb = Mysql(MYSQL_CONFIG)
        data = readonly(PATH)
        request = Request
    yield data, mydb, request
    mydb.close()


@pytest.fixture(scope='function')
def login(control):
    data, mydb, request = control
    response = request.initiate(method=data[0][2], url=data[0][3], json=data[0][4])
    return response.json()['msg']

