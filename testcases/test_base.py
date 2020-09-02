import pytest
from common.excel import Excel
from common.readconfig import MYSQL_CONFIG, PATH


@pytest.mark.base
class TestBase:

    def test_login(self, control):
        data, mydb, request = control
        for value in data:
            response = request.initiate(method=value[2], url=value[3], data=value[4])
            res = mydb.execute_sql('select * from base_car', 'select')
            pytest.assume(value[-2] == response.json()['msg'])
