import pytest
from common.excel import Excel

Excel().readExcel()
@pytest.mark.base
class TestBase:

    @pytest.mark.parametrize("data", ['aj', 'kobe'])
    def test_login(self, setup, data):
        print(data)
        print('testing')
