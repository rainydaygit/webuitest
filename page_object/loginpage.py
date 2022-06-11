#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from page.webpage import WebPage, sleep
from common.readelement import Element

login = Element('login')

class LoginPage(WebPage):
    """登录类"""

    def input_username(self, content):
        """输入用户名"""
        self.input_text(login['用户名'], txt=content)
        sleep()

    def input_password(self, content):
        """输入密码"""
        self.input_text(login['密码'], txt=content)
        sleep()

    def click_login(self):
        """点击登录按钮"""
        self.is_click(login['登录按钮'])
        sleep()

    def click_logout(self):
        """点击退出登录下拉按钮"""
        sleep(1)
        self.is_click(login['退出登录下拉'])
        sleep()
        self.is_click(login['退出登录按钮'])


    def alert_confirm(self):
        """弹窗确定"""
        if self.is_exists(login['弹窗确定按钮']):
            js = 'document.getElementsByClassName("el-button--default el-button--primary")[0].click();'
            self.js(script=js)
            sleep()
        else: pass

    def del_cookies(self):
        """清除浏览器cookies并刷新页面"""
        self.del_browser_cookies()
        self.refresh()


if __name__ == '__main__':
    pass