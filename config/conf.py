#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from utils import times
from selenium.webdriver.common.by import By
from utils.times import dt_strftime


class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'page_element')

    # 报告文件
    REPORT_FILE = os.path.join(BASE_DIR, 'report.html')

    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME
    }

    # # 邮件信息
    # EMAIL_INFO = {
    #     'username': 'jiezhu2@sfmail.sf-express.com',  # 切换成你自己的地址
    #     'password': 'zhujie369*',
    #     'smtp_host': 'mail.sfmail.sf-express.com',
    #     'smtp_port': 143
    # }
    #
    # # 收件人
    # ADDRESSEE = [
    #     'jiezhu2@sfmail.sf-express.com',
    # ]

    @property
    def screen_path(self):
        """截图目录"""
        screenshot_dir = os.path.join(self.BASE_DIR, 'screen_capture')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        now_time = dt_strftime("%Y%m%d%H%M%S")
        screen_file = os.path.join(screenshot_dir, "{}.png".format(now_time))
        return now_time, screen_file

    @property
    def log_path(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        return log_dir

    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file

    def element_file(self, name):
        """页面元素文件"""
        element_path = os.path.join(self.ELEMENT_PATH, '%s.yaml' % name)
        if not os.path.exists(element_path):
            raise FileNotFoundError("%s 文件不存在！" % element_path)
        return element_path

cm = ConfigManager()
if __name__ == '__main__':
    print(cm.BASE_DIR)
    print(cm.REPORT_FILE)
