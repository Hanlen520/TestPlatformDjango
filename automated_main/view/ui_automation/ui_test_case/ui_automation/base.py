# coding=utf-8
# @Time : 2019/1/17 16:16
# @Author : wangyinghao
# @Site :
# @File : base.py
# @Software: PyCharm

from selenium.webdriver import ActionChains
import random
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import pyperclip
import logging
from AutomatedTestPlatform import settings

logger = logging.getLogger('django')


class BaseCommon(object):

    def __init__(self, driver):
        self.driver = driver
        self.logs = logger

    """
    打开浏览器
    """

    def open_url(self, url):
        return self.driver.get(url)

    """
    浏览器后退按钮
    """

    def back(self):
        return self.driver.back()

    """
    浏览器前进按钮
    """

    def forward(self):
        return self.driver.forward()

    """
    关闭浏览器
    """

    def close(self):
        return self.driver.close()

    """
    刷新
    """

    def fresh(self):
        return self.driver.refresh()

    """
    send_keys输入
    """

    def send_keys(self, by, webElement, keys, webElements=None):
        if webElements is None:
            self.element(by, webElement).send_keys(keys)
        else:
            self.elements(by, webElement)[webElements].send_keys(keys)

    """
    send_key输入,可上传图片
    """

    def send_key(self, by, webElement, keys, webElements=None):
        if webElements is None:
            self.element(by, webElement).send_keys(keys)
        else:
            self.elements(by, webElement)[webElements].send_keys(keys)

    """
    重写switch_frame方法
    """

    def switch_frame(self, frame):
        # noinspection PyBroadException
        try:
            element = self.driver.switch_to_frame(frame)
            return element
        except Exception:
            self.logs.error("未找到元素" + frame)
            return False

    """
    切换alert弹窗
    """

    def switch_to_alert(self, by, webElement):
        # noinspection PyBroadException
        try:
            self.click(by, webElement)
            self.driver.switch_to.alert
        except Exception:
            self.logs.error("未找到元素" + webElement)

    """
    截图
    """

    def picture(self):
        # 生成年月日时分秒时间
        picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        directory_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        self.logs.info(os.getcwd())
        log_path = os.path.join(settings.BASE_DIR, 'uiPicture')
        try:
            File_Path = log_path + '\\' + directory_time + '\\'
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
                self.logs.info("目录新建成功：%s" % File_Path)
            else:
                self.logs.info("目录已存在！！！")
        except BaseException as msg:
            self.logs.info("新建目录失败：%s" % msg)

        try:
            url = self.driver.save_screenshot(log_path + '\\' + directory_time + '\\' + picture_time + '.png')
            self.logs.info("%s ：截图成功！！！" % url)
        except BaseException as pic_msg:
            self.logs.info("截图失败：%s" % pic_msg)

    """
    点击
    """

    def click(self, by, element, webElements=None):
        if webElements is None:
            return self.element(by, element).click()
        else:
            return self.elements(by, element)[webElements].click()

    """
    双击
    """

    def double_click(self, by, element, webElements=None):

        if webElements is None:
            return self.element(by, element).double_click()
        else:
            return self.elements(by, element)[webElements].double_click()

    """
    鼠标长按左键
    """

    def click_and_hold(self, by, element, webElements=None):
        if webElements is None:
            return self.element(by, element).click_and_hold()
        else:
            return self.elements(by, element)[webElements].click_and_hold()

    """
    selenium 获取网页Title
    """

    def get_page_title(self):
        return self.logs.info(self.driver.title)

    """
    获取当前URL
    """

    def get_current_url(self):
        return self.logs.info(self.driver.current_url)

    """
    设置超时时间
    """

    def set_timeout(self, times="60"):
        return self.driver.implicitly_wait(times)

    """
    设置窗口最大化
    """

    def set_max_window(self):
        return self.driver.maximize_window()

    """
    拖拽元素
    """

    def drag_and_drop(self, by, element, x, y, webElements=None):
        # noinspection PyBroadException

        if webElements is None:
            try:
                action = ActionChains(self.driver)
                dragger = self.element(by, element)
                action.drag_and_drop_by_offset(dragger, x, y).perform()
            except Exception:
                self.logs.error("拖拽元素失败" + element)
        else:
            try:
                action = ActionChains(self.driver)
                dragger = self.elements(by, element)[webElements]
                action.drag_and_drop_by_offset(dragger, x, y).perform()
            except Exception:
                self.logs.error("拖拽元素失败" + element)

    """
    滑动滚动条
    """

    def script(self, by, button, x, y, webElements=None):
        # noinspection PyBroadException
        try:
            button = self.element(by, button)
            action = ActionChains(self.driver)
            action.click_and_hold(button).perform()
            action.reset_actions()
            action.move_by_offset(x, y).perform()
        except Exception:
            self.logs.error("滑动滚动条失败" + button)
        if webElements is None:
            try:
                button = self.element(by, button)
                action = ActionChains(self.driver)
                action.click_and_hold(button).perform()
                action.reset_actions()
                action.move_by_offset(x, y).perform()
            except Exception:
                self.logs.error("滑动滚动条失败" + button)
        else:

            try:
                button = self.elements(by, button)[webElements]
                action = ActionChains(self.driver)
                action.click_and_hold(button).perform()
                action.reset_actions()
                action.move_by_offset(x, y).perform()
            except Exception:
                self.logs.error("滑动滚动条失败" + button)

    """
    元素高亮显示
    """

    def high_light(self, by, element):
        return self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                          self.element(by, element), "background: green; border: 2px solid red;")

    """
    鼠标悬浮
    """

    def mouse_suspension(self, by, element, webElements=None):

        if webElements is None:
        # noinspection PyBroadException
            try:
                mouse = self.element(by, element)
                ActionChains(self.driver).move_to_element(mouse).perform()
            except Exception:
                self.logs.error("鼠标悬浮失败" + element)
        else:
            try:
                mouse = self.element(by, element)[webElements]
                ActionChains(self.driver).move_to_element(mouse).perform()
            except Exception:
                self.logs.error("鼠标悬浮失败" + element)

    """
    随机数
    """

    def randomNumber(self):
        return random.sample('1234567890', 3)

    """
    鼠标单击（坐标）
    """

    def mouse_click(self, element):
        actions = ActionChains(self.driver)
        actions.click_and_hold(element).move_by_offset(65, 27).release().perform()
        time.sleep(2)
        actions.click_and_hold(element).move_by_offset(140, 30).release().perform()

    """
    切换窗口
    """

    def change_window_handle(self):
        # 输出当前窗口句柄
        # print(self.driver.current_window_handle)
        # 获取当前全部窗口句柄集合
        handles = self.driver.window_handles
        # 输出句柄集合
        # print(handles)
        for handle in handles:
            if handle != self.driver.current_window_handle:
                self.logs.info("switch to second window", handle)
        # self.driver.close()
        self.driver.switch_to.window(handle)
        time.sleep(5)
        self.logs.info("切换窗口成功")

    """
    查找元素
    """

    def element(self, by, value, seconds=10):
        if by == "id":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.by, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "class":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "name":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.NAME, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "css":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "linktext":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_element_located((By.LINK_TEXT, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "partial":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "tag":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_element_located((By.TAG_NAME, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "xpath":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_element_located((By.XPATH, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        else:
            self.logs.error("请输入适合的查找元素方式。。。")

    """
    查找元素组
    """
    def elements(self, by, value, seconds=10):

        if by == "id":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_all_elements_located((By.ID, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "class":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "name":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_all_elements_located((By.NAME, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "css":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "linktext":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_all_elements_located((By.LINK_TEXT, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "partial":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "tag":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        elif by == "xpath":
            # noinspection PyBroadException
            try:
                element = WebDriverWait(self.driver, seconds, 1).until(
                    EC.presence_of_all_elements_located((By.XPATH, value)))
                return element
            except Exception:
                self.logs.error("未找到元素" + value)
                return False
        else:
            self.logs.error("请输入适合的查找元素方式。。。")

    """
    js查找元素方式，或jQuery
    """

    def ExcuteJs(self, js):
        return self.driver.execute_script(js)

    """
    复制粘贴
    """
    def copy(self):
        a = pyperclip.paste()
        self.logs.info(a)
        js = "window.open('http://{}')".format(a)
        self.logs.info(js)
        self.driver.execute_script(js)

    """
    全选输入
    """
    def input(self, by, webElement, keys):
        self.element(by, webElement).send_keys(self.keys.CONTROL, 'a')
        self.element(by, webElement).send_keys(keys)

    """
    关闭新打开页面
    """
    def close_new_window(self, is_await=False):
        """
        :param is_await: 新打开窗口是否挂起,默认为打开后直接关闭
        """
        time.sleep(3)
        self.change_window_handle()
        if not is_await:
            self.driver.close()
            return self.change_window_handle()
        return

    """
    利用键盘清空输入框内容
    """
    def keyboard_clear_contents(self, by, value):
        time.sleep(2)
        self.element(by, value).send_keys(self.keys.CONTROL, 'a')
        self.element(by, value).send_keys(self.keys.DELETE)

    """
    回车
    """
    def enter(self, by, value):
        time.sleep(2)
        return self.element(by, value).send_keys(self.keys.ENTER)

    """
    鼠标事件(鼠标悬浮在mouse元素上，移动到x，y坐标并点击)
    """
    def mouse_suspension_click(self, by, element, x, y):
        mouse = self.element(by, element)
        actions = ActionChains(self.driver)
        # 鼠标悬浮在mouse元素上，移动到x，y坐标并点击
        actions.move_to_element(mouse).move_by_offset(x, y).click().perform()
        time.sleep(2)

    """
    获取元素的坐标
    """
    def get_element_coordinate(self, by, value):
        return self.element(by, value).location

    """
    获取元素的属性值
    """
    def get_element_value(self, by, value, attribute):
        return self.element(by, value).get_attribute(attribute)

    """
    获取元素的大小
    """
    def get_element_size(self, by, value):
        return self.element(by, value).size

    """
    检查元素是否可见
    """
    def get_element_is_displayed(self, by, value):
        return self.element(by, value).is_displayed()

    """
    检查元素是否被选中(一般用于单选或复选框)
    """
    def get_element_is_selected(self, by, value):
        return self.element(by, value).is_selected()

    """
    获取浏览器名字
    """
    def get_browser_name(self):
        return self.driver.name
