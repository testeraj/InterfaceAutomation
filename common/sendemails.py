import smtplib
import zipfile
import os
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Email(object):

    def __init__(self, config):
        self.mail_config = config
        self.attachment = MIMEMultipart()
        self.attachment['From'] = Header(self.mail_config['sender'])     # 发送邮箱地址
        self.attachment['To'] = Header(self.mail_config['receivers'])      # 收件箱地址
        self.attachment['Subject'] = Header('Test Report')                 # 主题

    @staticmethod
    def compress(source_file):
        if os.path.isdir(source_file):
            compressed_path = f'{source_file}.zip'
            with zipfile.ZipFile(compressed_path, 'w', zipfile.ZIP_DEFLATED) as f:
                for dirpath, dirnames, filenames in os.walk(source_file):
                    for filename in filenames:
                        f.write(os.path.join(dirpath, filename))
                f.close()
            return compressed_path
        elif os.path.isfile(source_file):
            return source_file
        else:
            raise FileNotFoundError('file or path does not exist')

    def send_mail(self, source):
        path = self.compress(source)
        text = MIMEText(self.mail_config['content'], 'plain', 'utf-8')
        atta = MIMEApplication(open(path, 'rb').read())
        atta.add_header('Content-Disposition', 'attachment', filename=path.split('/')[-1])
        self.attachment.attach(text)
        self.attachment.attach(atta)
        mail_server = smtplib.SMTP_SSL(self.mail_config['host'], self.mail_config['port'])
        # mail_server.set_debuglevel(1)     # 可以打印出和SMTP服务器交互的所有信息
        # print(mail_server.ehlo())           # 使用ehlo指令向esmtp服务器确认你的身份
        mail_server.login(self.mail_config['sender'], self.mail_config['passwd'])
        mail_server.sendmail(self.mail_config['sender'], self.mail_config['receivers'], self.attachment.as_string())
        mail_server.quit()
