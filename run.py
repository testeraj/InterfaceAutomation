import os
import yaml
import pytest


def __getconf():
    with open(file='config.yaml', mode='r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result


CONFIG = __getconf()


if __name__ == '__main__':
    pytest.main(['-v', '-s', 'testcases'])
