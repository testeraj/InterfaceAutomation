import pytest
from common.excel import Excel
from common.request import Request
from common.readconfig import PATH


test_data = Excel(PATH).readExcel('A2')
@pytest.mark.base
class TestBase:

    @pytest.mark.parametrize("data", test_data)
    def test_login(self, setup, data):
        response = Request.initiate(method=data[2], url=data[3], json=data[4])
        a = response.text
        pytest.assume(data[-2] == a['msg'])


