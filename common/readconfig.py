#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import configparser
from config.conf import cm

class ReadConfig(object):
    """配置文件"""

    def __init__(self):
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(cm.ini_file, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(cm.ini_file, 'w') as f:
            self.config.write(f)

    @property
    def url(self):
        return self._get('PROJECT', 'HOST')

    @property
    def project_name(self):
        return self._get('PROJECT', 'NAME')

    @property
    def project_executor(self):
        return self._get('PROJECT', 'EXECUTOR')

    @property
    def project_department(self):
        return self._get('PROJECT', 'DEPARTMENT')

    def email_smtp_server(self):
        return self._get('EMAIL', 'SMTP_SERVER')

    def email_port(self):
        return self._get('EMAIL', 'PORT')

    def email_sender(self):
        return self._get('EMAIL', 'SENDER')

    def email_password(self):
        return self._get('EMAIL', 'PASSWORD')

    def email_receiver(self):
        return self._get('EMAIL', 'RECEIVER')

    @property
    def email_switch(self):
        return self._get('EMAIL', 'SWITCH')

ini = ReadConfig()

if __name__ == '__main__':
    print(ini.url)
