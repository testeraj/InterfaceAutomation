import pytest


@pytest.mark.base
class TestBase:

    def test_login(self, control):
        data, mydb, request = control
        for value in data:
            response = request.initiate(method=value[2], url=value[3], data=value[4])
            pytest.assume(value[-2] == response.json()['msg'])
