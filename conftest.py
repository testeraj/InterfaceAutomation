import pytest
from common.excel import Excel
from common.readconfig import PATH


@pytest.fixture(scope='session', autouse=True)
def control():
    excel = Excel(PATH)
    yield excel
    excel.close()


@pytest.fixture(scope='function')
def data(control):
    return control.readExcel('A2')
