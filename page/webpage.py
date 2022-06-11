#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
selenium基类
本文件存放了selenium基类的封装方法
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
# from selenium import webdriver

from config.conf import cm
from utils.times import sleep
from utils.logger import log

class WebPage(object):
    """selenium基类"""

    def __init__(self, driver):
        # self.driver = webdriver.Chrome()
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, self.timeout)

    def open_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
        # set_page_load_timeout设置页面完全加载的超时时间，完全加载即页面全部渲染，异步同步脚本都执行完成
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            # implicitly_wait识别对象的超时时间，如果在设置的时间内没有找到就抛出一个NoSuchElement异常
            # self.driver.implicitly_wait(5)
            log.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(cm.LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素，并高亮显示"""
        element = WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)
        STYLE = "background: yellow; border: 2px solid red;"  # 高亮的样式
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, STYLE)
        return element

    def focus(self):
        """聚焦元素"""
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def find_elements(self, locator):
        """查找多个相同的元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, txt):
        """输入(输入前先清空)"""
        sleep()
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)
        log.info("输入文本：{}".format(txt))

    def is_click(self, locator):
        """点击"""
        self.find_element(locator).click()
        sleep()
        log.info("点击元素：{}".format(locator))

    def is_exists(self, locator):
        """元素是否存在(DOM)"""
        try:
            WebPage.element_locator(lambda *args: EC.presence_of_element_located(args)(self.driver), locator)
            log.info("元素存在！")
            return True
        except EC.NoSuchElementException:
            log.info("元素不存在！")
            return False

    def alert_exists(self):
        """判断弹框是否出现，并返回弹框的文字"""
        alert = EC.alert_is_present()(self.driver)
        if alert:
            text = alert.text
            log.info("Alert弹窗提示为：%s" % text)
            alert.accept()
            return text
        else:
            log.error("没有Alert弹窗提示!")

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取文本：{}".format(_text))
        return _text

    def get_alert_text(self):
        """获取alert提示文本
        不是通用的，可能不生效"""
        alert_text = self.find_element(('class', 'el-message__content')).get_attribute('textContent')
        log.info("获取提示文本：{}".format(alert_text))
        return alert_text

    def js(self, script):
        """
        执行JavaScript脚本。
        用法
        driver.js("window.scrollTo(200,1000);")
        """
        self.driver.execute_script(script)
        log.info("执行js脚本：{}!".format(script))

    def send_keyBoardsEvent(self, locator, keyEvent=Keys.ENTER):
        """
        Operation send key board event on target.
        操作发送目标上的键盘事件。

      * 如果需要操作键盘事件，则需在启动脚本导入Keys类：from selenium.webdriver.common.keys import Keys
        常用组合键：
        send_keys(Key.CONTROL,'a') #全选（Ctrl+A）
        send_keys(Key.CONTROL,'c') #复制（Ctrl+C）
        send_keys(Key.CONTROL,'x') #剪切（Ctrl+X）
        send_keys(Key.CONTROL,'v') #粘贴（Ctrl+V）
        注意：send_keys有两个参数

        常用的非组合键：
        回车键 Keys.ENTER
        删除键 Keys.BACK_SPACE
        空格键 Keys.SPACE
        制表键 Keys.TAB
        回退键 Keys.ESCAPE
        刷新键 Keys.F5

        Usage:
        用法
        driver.send_keyBoardsEvent("id=kw",Keys.ENTER)
        """
        self.find_element(locator).send_keys(keyEvent)
        log.info("键盘输入：{}".format(keyEvent))


    def get_title(self):
        """
        获取window标题
        用法
        driver.get_title()
        """
        title = self.driver.title
        log.info("获取浏览器标题：{}".format(title))
        return title

    def get_url(self):
        """
        获取当前页面的URL地址。
        用法
        driver.get_url()
        """
        url = self.driver.current_url
        log.info("获取浏览器url：{}".format(url))
        return url

    def scroll_top(self):
        """滚动到顶部"""
        js_top = "window.scrollTo(0,0)"
        self.js(js_top)

    def scroll_foot(self):
        """滚动到底部"""
        js_foot = "window.scrollTo(0,document.body.scrollHeight)"
        self.js(js_foot)

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        # self.driver.implicitly_wait(30)
        log.info("刷新页面成功！")

    def del_browser_cookies(self):

        self.driver.delete_all_cookies()
        log.info("清除浏览器cookies成功！")

if __name__ == "__main__":
    pass

