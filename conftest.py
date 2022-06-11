#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import base64
import pytest
import allure
from py.xml import html
from selenium import webdriver

from config.conf import cm
from common.readconfig import ini
from utils.times import timestamp
from utils.send_email import se
from utils.logger import log
from page_object.loginpage import LoginPage

driver = None
# 默认浏览器驱动为chrome，可以设置"ie"或者"firefox"
webdri = 'chrome'

# setup前置操作，启动浏览器，并最大化
@pytest.fixture(scope='session', autouse=True)
def drivers(request, dri=webdri):
    global driver
    if dri.lower() == 'chrome':
        # 静默启动，后台执行
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # driver = webdriver.Chrome(chrome_options=option)
        driver = webdriver.Chrome()
    elif dri.lower() == 'firefox':
        driver = webdriver.Firefox()
    elif dri.lower() == 'ie':
        driver = webdriver.Ie()
    driver.maximize_window()

    # teardown清理，退出浏览器
    def fn():
        driver.quit()
    request.addfinalizer(fn)
    return driver

@pytest.fixture(scope='session')
def login(drivers, username="admin", password="123456"):
    """登录"""
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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = _capture_screenshot()
            if screen_img:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


def pytest_html_report_title(report):
    report.title = ini.project_name + "项目自动化测试报告"


def pytest_configure(config):
    config._metadata.clear()
    config._metadata['测试项目: '] = ini.project_name
    config._metadata['测试地址: '] = ini.url


def pytest_html_results_summary(prefix, summary, postfix):
    # prefix.clear() # 清空summary中的内容
    prefix.extend([html.p("所属部门: " + ini.project_department)])
    prefix.extend([html.p("测试执行人: " + ini.project_executor)])

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """收集测试结果"""
    result = {
        "total": terminalreporter._numcollected,
        'passed': len(terminalreporter.stats.get('passed', [])),
        'failed': len(terminalreporter.stats.get('failed', [])),
        'error': len(terminalreporter.stats.get('error', [])),
        'skipped': len(terminalreporter.stats.get('skipped', [])),
        # terminalreporter._sessionstarttime 会话开始时间
        'total times': timestamp() - terminalreporter._sessionstarttime
    }
    # 默认不发送邮件
    if ini.email_switch == '0':
        log.info("发送邮件功能关闭，不发送邮件！可在config.ini里开启。")
    elif ini.email_switch == '1':
        se.send_email_multipart()
    pass
    # 有失败的测试用例时才发送报告
    # if result['failed'] or result['error']:
    #     if ini.email_switch == '0':
    #         log.info("发送邮件功能关闭，不发送邮件！可在config.ini里开启。")
    #     elif ini.email_switch == '1':
    #         se.send_email_multipart()
    #     pass

def _capture_screenshot():
    """截图保存为base64"""
    now_time, screen_file = cm.screen_path
    driver.save_screenshot(screen_file)
    allure.attach.file(screen_file,
                       "失败截图{}".format(now_time),
                       allure.attachment_type.PNG)
    with open(screen_file, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()
