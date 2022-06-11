#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common.readconfig import ini
from utils.logger import log
from utils.times import dt_strftime
from config.conf import cm

subject = dt_strftime("%Y-%m-%d %H:%M:%S") + '最新的自动化测试报告'
class SendEmail():
    """
    发送带附件的邮件
    """
    def __init__(self, receiver=ini.email_receiver()):
        # 邮件配置：发件人，收件人，服务器端口
        self.smtpserver = ini.email_smtp_server()
        self.port = ini.email_port()
        self.sender = ini.email_sender()
        self.pwd = base64.b64decode(ini.email_password()).decode("utf-8")
        # 收件人接收多个
        self.receiver = receiver.split(',')

    def send_email_text(self, content, subject=subject):
        """发送文本邮件"""
        # 邮件内容：主题，正文
        msg = MIMEText(content, 'html', 'utf-8')

        msg['from'] = self.sender
        msg['to'] = ';'.join(self.receiver)
        msg['subject'] = subject

        #发送邮件：实例化SMTP，链接服务器，登录服务器，发送邮件
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtpserver)
            smtp.login(self.sender, self.pwd)
        except:
            smtp = smtplib.SMTP_SSL(self.smtpserver, self.port)
            smtp.login(self.sender, self.pwd)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()

    def send_email_multipart(self, fpath=cm.REPORT_FILE, subject=subject):
        """发送带附件的邮件"""
        msg = MIMEMultipart()
        msg['from'] = self.sender
        msg['to'] = ';'.join(self.receiver)
        msg['subject'] = subject

        # 发送带附件的邮件
        with open(fpath, 'rb') as f:
            mail_body = f.read()

        # 正文
        content = MIMEText(mail_body, 'html', 'utf-8')
        msg.attach(content)
        # 附件
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename="test_report.html"'
        msg.attach(att)

        #发送邮件：实例化SMTP，链接服务器，登录服务器，发送邮件
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtpserver)
            smtp.login(self.sender, self.pwd)
        except Exception as ec:
            log.error('邮箱登录失败！失败原因：{}', format(ec))
            # QQ邮箱要使用SSL
            # smtp = smtplib.SMTP_SSL(self.smtpserver, self.port)
            # smtp.login(self.sender, self.pwd)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        log.info('邮件发送成功！')
        smtp.quit()

se = SendEmail()

if __name__ == '__main__':
    se.send_email_multipart()
