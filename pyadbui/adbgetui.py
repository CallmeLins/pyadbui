# coding=utf-8
import sys
import re
import logging
import traceback
from lxml import etree
from lxml.etree import tostring

short_keys = {'id': 'resource-id', 'class_': 'class', 'klass': 'class', 'desc': 'content-desc'}


class GetUI(object):
    def __init__(self, adbext):
        self.adbext = adbext
        self.keys = None
        self.xml = None
        self.ocr = None
        self.image = None

    def get_ui_by_attr(self, is_contains=True, is_update=True, try_count=1, **kwargs):
        """
        通过节点的属性获取节点
        :param is_contains:
        :param is_update:
        :param try_count:
        :param kwargs:
        :return:
        """
        uis = self.get_uis_by_attr(is_contains=is_contains, is_update=is_update, try_count=try_count, **kwargs)
        return uis[0] if uis else None

    def get_uis_by_attr(self, is_contains=True, is_update=True, try_count=1, **kwargs):
        """
        通过节点的属性获取节点
        :param try_count:
        :param is_contains: 是否使用模糊查找
        :param is_update:
        :param kwargs:
        :return: 
        """
        for key in list(kwargs):
            if key in short_keys:
                kwargs[short_keys[key]] = kwargs.pop(key)
        if is_contains:
            s = list(map(lambda x: "contains(@{}, '{}')".format(x, kwargs[x]), kwargs))
            xpath = './/*[{}]'.format(' and '.join(s))
        else:
            s = list(map(lambda key: "[@{}='{}']".format(key, kwargs[key]), kwargs))
            xpath = './/*{}'.format(''.join(s))
        uis = self.get_uis_by_xpath(xpath, is_update=is_update, try_count=try_count)
        return uis

    def get_ui_by_xpath(self, xpath, is_update=True, try_count=1):
        uis = self.get_uis_by_xpath(xpath, is_update, try_count=try_count)
        return uis[0] if uis else None

    def get_uis_by_xpath(self, xpath, is_update=True, try_count=1):
        """
        通过xpath查找节点
        :param try_count:
        :param xpath:
        :param is_update: 
        :return: 
        """
        elements = []
        for index in range(try_count):
            if is_update:
                xml_str = self.adbext.dump()  # 获取xml文件
                self.__init_xml(xml_str)

            xpath = xpath.decode('utf-8') if sys.version_info[0] < 3 else xpath
            elements = self.xml.xpath(xpath)
            if elements:
                elements = [self.get_ui_by_element(x) for x in elements]
                break

        return elements

    def get_ui_by_element(self, element):
        bounds = element.get('bounds')
        x1, y1, x2, y2 = re.compile(r"-?\d+").findall(bounds)
        ui = UI(self.adbext, x1, y1, x2, y2)
        ui.element = element
        text = element.get('text')
        if not text:
            text = element.get('content-desc')
        ui.text = text.encode('utf-8') if self.adbext.util.is_py2 and not isinstance(text, str) else text
        return ui

    def __init_xml(self, xml_str):
        parser = etree.XMLParser(huge_tree=True)
        self.xml = etree.fromstring(xml_str, parser=parser)
        for element in self.xml.findall('.//node'):
            element.tag = element.get('class').split('.')[-1].replace('$', '')  # 将每个node的name替换为class值, 和uiautomator里显示的一致


class UI:
    def __init__(self, adbext, x1, y1, x2, y2):
        self.__adbext = adbext
        self.x1 = int(x1)  # 左上角 x
        self.y1 = int(y1)  # 左上角 y
        self.x2 = int(x2)  # 右下角 x
        self.y2 = int(y2)  # 右下角 y
        self.width = self.x2 - self.x1  # 元素宽
        self.height = self.y2 - self.y1  # 元素高
        self.x = self.x1 + int(self.width / 2)
        self.y = self.y1 + int(self.height / 2)
        self.text = None  # 元素文本
        self.element = None  # 元素对应的 lxml element, ocr无效

    def get_element_str(self):
        return tostring(self.element)

    def get_value(self, key):
        # 返回 lxml element 属性对应的值
        if key in short_keys:
            key = short_keys[key]
        return self.element.get(key)

    def click(self):
        # 点击元素的中心点
        self.__adbext.click(self.x, self.y)
