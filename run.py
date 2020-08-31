import os
import yaml
import pytest
from common.readconfig import PATH
from common.excel import Excel

data = Excel(PATH).readExcel('A2')






if __name__ == '__main__':
    pytest.main(['-v', '-s', 'testcases'])
