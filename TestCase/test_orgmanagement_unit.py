#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure
from utils.logger import log
from common.readconfig import ini
from page_object.orgmanagement_unit_page import OrgmanagementUnitPage

@allure.feature("测试2038基础数据-单位目录模块")
class TestOrgmanagementUnit:
    @allure.story("测试2038打开单位目录用例")
    def test_open_unit(self, drivers, login):
        """打开单位目录页面"""
        oup = OrgmanagementUnitPage(drivers)
        oup.open_url(ini.url + 'baseData/orgManagement/unit')
        url = oup.get_url()
        assert 'unit' in url
        log.info("打开单位目录页面成功！")

    @allure.story("测试2038打开用户单位组织结构用例")
    def test_open_orgnrltn(self, drivers, login):
        """打开用户单位组织结构页面"""
        oup = OrgmanagementUnitPage(drivers)
        oup.open_url(ini.url + 'baseData/orgManagement/orgnRltn')
        url = oup.get_url()
        assert 'orgnRltn' in url
        log.info("打开用户单位组织结构页面成功！")

    @allure.story("测试2038打开储存单位管理结构用例")
    def test_open_orgnsbrl(self, drivers, login):
        """打开单位储存单位管理结构页面"""
        oup = OrgmanagementUnitPage(drivers)
        oup.open_url(ini.url + 'baseData/orgManagement/orgnSbrl')
        url = oup.get_url()
        assert 'orgnSbrl' in url
        log.info("打开储存单位管理结构页面成功！")

if __name__ == '__main__':
    pytest.main(['TestCase/test_orgmanagement_unit.py'])