# pyadbui
![Windows](https://img.shields.io/badge/Windows-0078D6)
![Python](https://img.shields.io/badge/python-3670A0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

pyadbui 所有的功能都是通过 adb 命令, pyadbui 的特色是可以通过 xpath, ocr 获取 ui 元素。

## 简介
UiAutomator2 是 Python 常用的用来做安卓自动化测试的一个 python 库, 但是目前处于低活跃度的开发中, 已经很久不再更新, 且不够稳定

我们希望测试逻辑能够用 Python 编写, 且通过安卓原生的 UiAutomator 获取 UI 元素, 然后通过 adb 原生的指令进行控制。
这里要非常感谢 tango (@hao1032), 他将这个想法实现了出来（见 hao1032/adbui）, 原理是直接调用 uiautomator dump 当前 UI 为 xml 再将解析部分封装成Python库。 
因为 hao1032/adbui 这个库, 已经很久不见更新。所以我们直接fork了一个版本, 为了方便做区分我们重新命名为 pyadbui

## 进度
- 将带 ocr 识别的版本移入 develope 分支
- master 分支中仅保留简单的获取属性的方法

## 安装
    直接通过 wheel 进行安装
    pip install pyadbui

## 要求
- 在命令中可以使用 adb 命令, 即adb已经配置到环境变量
- adb 的版本最好是 >= 1.0.39, 用老版本的 adb 可能会有一些奇怪的问题
- 依赖的库：lxml 解析 xml, function_timeout

## 说明
- pyadbui 当前还在完善, bug 和建议请直接在 github 反馈
- 主要在 win10, python3 环境使用, 其他环境可能有问题

## import and init
    from adbui import Device

    d = Device('123abc')  # 手机的sn号, 如果只有一个手机可以不写

## pyadbui 可以分为 3 个部分
**util 负责执行完整的命令**

  - **cmd** 用来执行系统命令
  
        d.util.cmd('adb -s 123abc reboot')
        out = d.util.cmd('ping 127.0.0.1')
    
  - **adb** 用来执行 adb 命令
  
        d.util.adb('install xxx.apk')
        d.util.adb('uninstall com.tencent.mtt')
    
  - **shell** 用来执行 shell 命令
  
        d.util.shell('pm clear com.tencent.mtt')
        d.util.shell('am force-stop com.tencent.mtt')

**adbext 对常用 adb 命令的封装, 下面列出部分操作（可在 pyadbui/adbext.py 文件自行增加需要的操作）**

  - **screenshot**
   
        d.adbext.screenshot() # 截图保存到系统临时目录, 也可指定目录
        
  - **click**
  
        d.adbext.click(10, 32)  # 执行一个点击事件 
        
  - **input**
  
        d.adbext.input('pyadbui')  # 输入文本 
        
  - **back**
  
        d.adbext.back()  # 发出 back 指令 


**getui 可以通过多种方式获取 UI**
  - **by attr** 通过在 uiautomator 里面看到的属性来获取
  
        ui = d.get_ui_by_attr(text='设置', desc='设置')  # 支持多个属性同时查找

        ui = d.get_ui_by_attr(text='设', is_contains=True)  # 支持模糊查找

        ui = d.get_ui_by_attr(text='设置', is_update=False)  # 如果需要在一个界面上获取多个 UI,  再次查找时可以设置不更新xml文件和截图, 节省时间

        ui = d.get_ui_by_attr(class_='android.widget.TextView')  # class 在 python 中是关键字, 因此使用 class_ 代替

        ui = d.get_ui_by_attr(desc='fffffff')  # 如果没有找到, 返回 None;如果找到多个返回第一个

        ui = d.get_uis_by_attr(desc='fffffff')  # 如果是 get uis 没有找到, 返回空的 list
    
  - **by xpath** 使用 xpath 来获取
  
        mic_btn = d.get_ui_by_xpath('.//FrameLayout/LinearLayout/RelativeLayout/ImageView[2]')  # 获取麦克风按钮
        mic_btn.click()  # 点击麦克风按钮
        
        # pyadbui 使用 lxml 解析 xml 文件, 因此 by xpath 理论上支持任何标准的 xpth 路径。
        # 这里有一篇 xpath 使用的文章：https://cuiqingcai.com/2621.html
        
        # 另外获取的 ui 对象实际是一个自定义的 UI 实类, ui 有一个 element 的属性, element 就是 lxml 里面的 Element 对象, 
        # 因此可以对 ui.element 执行 lxml 的相关操作。
        # lxml element 对象的文档：http://lxml.de/api/lxml.etree._Element-class.html
        
        scan_element = ui.element.getprevious()  # 获取麦克风的上一个 element, 即扫一扫按钮
        scan_btn = d.get_ui_by_element(scan_element)  # 使用 element 实例化 UI
        scan_btn.click()  # 点击扫一扫按钮

## Change Log
20231105 version 4.6.0
- fork 新仓库
- master 分支移除 ocr 功能
