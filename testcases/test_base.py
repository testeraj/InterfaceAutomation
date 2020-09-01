import pytest
from common.excel import Excel
from common.request import Request
from common.readconfig import PATH


@pytest.fixture(scope='function')
def data(control):
    print(control)
    print(control.param)
    return control.param


@pytest.mark.base
class TestBase:

    @pytest.mark.parametrize("data")
    def test_login(self, data):
        a = data
        print(data)
        response = Request.initiate(method=data[2], url=data[3], json=data[4])
        a = response.text
        pytest.assume(data[-2] == a['msg'])
