import pytest
from filelock import FileLock
from common.excel import Excel
from common.mysqldb import Mysql
from common.request import Request
from common.sendemails import Email
from common.readconfig import MYSQL_CONFIG, PATH, EMAIL_CONFIG


@pytest.fixture(scope='session', autouse=True)
def control():
    with FileLock("session.lock"):
        email = Email(EMAIL_CONFIG)
        mydb = Mysql(MYSQL_CONFIG)
        request = Request
        excel = Excel(PATH)
        data = excel.readExcel()
        data.pop(0)
    yield data, mydb, request
    excel.close()
    mydb.close()
    email.send_mail('F:/InterfaceAutomation/report.html')


@pytest.fixture(scope='function')
def login(control):
    data, mydb, request = control
    response = request.initiate(method=data[0][2], url=data[0][3], json=data[0][4])
    return response.json()['token']

