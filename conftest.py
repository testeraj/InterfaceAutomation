import pytest
from filelock import FileLock
from common.excel import Excel
from common.readconfig import PATH


@pytest.fixture(scope='session', autouse=True)
def control():
    with FileLock("session.lock"):
        excel = Excel(PATH)
    yield excel
    excel.close()


@pytest.fixture(scope='function')
def data(control):
    return control.readExcel('A2')
