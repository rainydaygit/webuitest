# WEB-UI 自动化测试框架(Python)

---

## 框架设计

- python
- pytest
- selenium
- POM页面对象模型（Page Object Model）
- allure测试报告

---

## 目录结构

    common                 ——公共类
    Page                   ——基类
    PageElements           ——页面元素类
    PageObject             ——页面对象类
    TestCase               ——测试用例
    utils                  ——工具类
    config                 ——配置文件
    conftest.py            ——pytest胶水文件
    pytest.ini             ——pytest配置文件
    run_case.py            ——主运行文件

---

## 运行项目

### 环境配置

* 安装`Python3`，并配置好环境变量
* 安装与本机浏览器版本对应的`webdriver`驱动
* 下载安装最新版的`allure`，配置好环境变量

### 安装依赖

```shell
pip install -r requirements.txt
```

### 执行主文件

* 在项目根目录执行`run_case.py`文件即可运行项目


# allure参数说明


- pytest --alluredir `result-path`
    - --clean-alluredir 清除历史生成记录
- allure generate `result-path`
    - -c 生成报告前删除上一次生成的报告
    - -o 指定生成的报告目录
- allure open `report-path`

# pytest.ini参数说明

* --reruns 1 失败重跑
* --html=report/report.html --self-contained-html 生成pytest-html带样式的报告
* -s 输出我们用例中的调式信息
* -q 安静的进行测试
* -v 可以输出用例更加详细的执行信息，比如用例所在的文件及用例名称等
* --lf, --last-failed 只重新运行上次运行失败的用例（或如果没有失败的话会全部跑）
* --ff, --failed-first 运行所有测试，但首先运行上次运行失败的测试（这可能会重新测试，从而导致重复的fixture setup/teardown）
* addopts = --html=report.html --self-contained-html

