import yaml


with open(file='F:/InterfaceAutomation/config.yaml', mode='r', encoding='utf-8') as f:
    CONFIG = yaml.load(f.read(), Loader=yaml.FullLoader)

LOG_CONFIG = CONFIG['Log']
MYSQL_CONFIG = CONFIG['MySQL']
SERVER_CONFIG = CONFIG['Server']
EMAIL_CONFIG = CONFIG['Email']
PATH = CONFIG['File']['path']
