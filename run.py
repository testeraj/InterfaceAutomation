import os
import pytest

if __name__ == '__main__':

    pytest.main()
    os.system('allure generate allure-result -o allure-report --clean')
# os.system('allure serve ./allure-result')

