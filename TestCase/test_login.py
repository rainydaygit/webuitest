#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import pytest
import allure
from utils.logger import log
from common.readconfig import ini
from page_object.loginpage import LoginPage

@allure.feature("测试2038登录模块")
class TestLogin:
    # @pytest.fixture(scope='function', autouse=True)
    # def open_index(self, drivers):
    #     """打开登录页"""
    #     login = LoginPage(drivers)
    #     indexurl = ini.url + 'login'
    #     login.open_url(indexurl)


    @allure.story("测试2038登录用例")
    # @pytest.mark.skip("跳过登录的测试用例！")
    @pytest.mark.parametrize("username,password", [
        ("jwzg", "123456"),
        ("jzfg1", "123456"),
        ("jzfg2", "123456"),
    ])
    def test_login(self, drivers, username, password):
        """登录测试用例"""
        login = LoginPage(drivers)
        login.del_cookies()
        indexurl = ini.url + 'login'
        login.open_url(indexurl)
        login.input_username(username)
        login.input_password(password)
        login.click_login()
        login.alert_confirm()
        url = login.get_url()
        assert 'dashboard' in url
        log.info('登录成功！')

    # @allure.story("测试2038退出登录用例")
    # def test_logout(self, drivers):
    #     """退出测试用例"""
    #     login = LoginPage(drivers)
    #     login.click_logout()
    #     login.alert_confirm()
    #     assert '退出成功' in login.get_alert_text()
    #     log.info('退出成功！')

if __name__ == '__main__':
    pytest.main(['TestCase/test_login.py'])