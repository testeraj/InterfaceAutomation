import pytest


@pytest.fixture(scope='session', autouse=True)
def setup():
    print('1111')
    yield
    print('2222')