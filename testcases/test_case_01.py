import pytest


@pytest.mark.parametrize("data", ['aj', 'kobe'])
def test_case_01(setup, data):
    print(data)
    print('testing')
