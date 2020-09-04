import os
import pytest
from common.sendemails import Email
from common.readdata import EMAIL_CONFIG


if __name__ == '__main__':
    path3 = 'F:/InterfaceAutomation/report.html'
    if os.path.exists(path3):
        os.remove(path3)
    pytest.main()
    os.system('allure generate allure-result -o allure-report')
    # Email(EMAIL_CONFIG).send_mail('F:/InterfaceAutomation/report.html')
    # os.system('allure serve ./allure-result')

