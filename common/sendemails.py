import smtplib
import zipfile
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
from common.log import LogManage


class Email(object):

    def __init__(self):

        self.mail_config = {
            'host' : 'smtp.163.com',    #smtp服务器
            'port' : 465,    #smtp端口
            'passwd' : 'YZZNFHGRPVEVGENC',  #邮箱密码
            'sender' : 'x1124292446@163.com',   #发件人邮箱
            'receivers' : 'x1124292446@163.com',    #收件人邮箱
            'content' : '来自testeraj的测试报告，请查收！ps：详情见附件',   #邮件内容
        }
        self.attachment = MIMEMultipart()

    @staticmethod
    def zip_file():
        src_dir = './report'
        zip_name = src_dir + '.zip'
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as f:
            for dirpath, dirnames, filenames in os.walk(src_dir):
                for filename in filenames:
                    f.write(os.path.join(dirpath, filename))
            f.close()

    @LogManage()
    def send_mail(self):
        Email().zip_file()
        text = MIMEText(self.mail_config['content'], 'plain', 'utf-8')
        try:
            atta = MIMEApplication(open('./reports.zip', 'rb').read())
            atta.add_header('Content-Disposition', 'attachment', filename='report.zip')
        except BaseException as e:
            return e
        self.attachment.attach(text)
        self.attachment.attach(atta)
        # 发送邮箱地址
        self.attachment['From'] = Header(self.mail_config['sender'])
        # 收件箱地址
        self.attachment['To'] = Header(self.mail_config['receivers'])
        # 主题
        self.attachment['Subject'] = Header('Test Report')
        mail_server = smtplib.SMTP_SSL(self.mail_config['host'], self.mail_config['port'])
        # mail_server.set_debuglevel(1)
        # print(mail_server.ehlo())
        mail_server.login(self.mail_config['sender'], self.mail_config['passwd'])
        mail_server.sendmail(self.mail_config['sender'], self.mail_config['receivers'], self.attachment.as_string())
        mail_server.quit()


if __name__ == '__main__':
    email = Email()
    email.send_mail()