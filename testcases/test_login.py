import pytest


@pytest.mark.base
class TestLogin:

    @pytest.mark.parametrize('data', )
    def test_login(self, control, data):
        logger, mydb, request = control
        response = request.initiate(method=data[2], url=data[3], data=data[4], headers=[-3])
        pytest.assume(data[-2] == response.json()['msg'])
