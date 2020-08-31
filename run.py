import os
import pytest


pytest.main()

os.system('allure generate allure-result -o allure-report --clean')
os.system('allure serve ./allure-result')

