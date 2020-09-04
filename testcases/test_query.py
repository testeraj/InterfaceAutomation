import pytest
from common.readdata import DATA, IP


@pytest.mark.other
class TestQuery:

    @pytest.mark.parametrize('args', DATA)
    def test_query(self, control, login, args):
        logger, mydb, request = control
        response = request.initiate(method=args[3], url=IP+args[4], data=args[5], headers=login)
        pytest.assume(args[-2] == response.json()['code'])
