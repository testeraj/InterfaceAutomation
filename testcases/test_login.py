import pytest
from common.readdata import LOGIN, IP


@pytest.mark.login
class TestLogin:

    @pytest.mark.parametrize('args', LOGIN)
    def test_login(self, control, args):
        logger, mydb, request = control
        response = request.initiate(method=args[3], url=IP+args[4], data=args[5], headers=args[-3])
        pytest.assume(args[-2] == response.json()['msg'])

