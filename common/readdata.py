import yaml
from common.excel import readonly

with open(file='F:/InterfaceAutomation/config.yaml', mode='r', encoding='utf-8') as f:
    CONFIG = yaml.load(f.read(), Loader=yaml.FullLoader)

LOG_CONFIG = CONFIG['Log']
MYSQL_CONFIG = CONFIG['MySQL']
SERVER_CONFIG = CONFIG['Server']
EMAIL_CONFIG = CONFIG['Email']
PATH = CONFIG['File']
IP = CONFIG['Server']
DATA = [v for v in readonly(PATH) if v[0] != 'Login']
LOGIN = [v for v in readonly(PATH) if v[0] == 'Login']
