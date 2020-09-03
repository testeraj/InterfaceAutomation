import pytest
from common.excel import readonly
from common.readconfig import PATH, IP

data = readonly(PATH)


@pytest.mark.query
class TestQuery:

    @pytest.mark.parametrize('args', data)
    def test_query(self, control, login, args):
        print(login)
        logger, mydb, request = control
        response = request.initiate(method=args[3], url=IP+args[4], data=args[5], headers=args[-3])
        pytest.assume(args[-2] == response.json()['msg'] or response.json()['code'])
