import sys
from pyadbui import Device
from logging import Logger as logger

Res = {'OK': 0, 'ERR': -1, 'EXCEPTION': -2}

class AdbHelper():

    def __init__(self, adbid=None):
        self.adbid = adbid
        if self.adbid is not None:
            self.d = Device(self.adbid)
        else:
             self.d = Device()

    def FindElementById(self, resouceid:str):
        res = Res['ERR']
        try:
            logger.debug(f'Try to find resourceid element {resouceid}')
            ui = self.d.get_ui_by_attr(id=resouceid)
            if ui is not None:
                res = Res['OK']
                logger.debug(f'Found expect element {resouceid}')
            else:
                logger.debug(f'Not found expect element {resouceid}')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res

    def ClickElementById(self, resouceid:str):
        res = Res['ERR']
        try:
            logger.debug(f'Try to click resourceid element {resouceid}')
            ui = self.d.get_ui_by_attr(id=resouceid)
            if ui is not None:
                ui.click()
                res = Res['OK']
                logger.debug(f'Click expect element {resouceid} success')
            else:
                logger.debug(f'Not found expect element {resouceid}')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res

    def FindElementByText(self, text:str):
        res = Res['ERR']
        try:
            logger.debug(f'Try to find text element {text}')
            ui = self.d.get_ui_by_attr(text=text)
            if ui is not None:
                res = Res['OK']
                logger.debug(f'Found expect element {text}')
            else:
                logger.debug(f'Not found expect element {text}')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res

    def ClickElementByText(self, text:str):
        res = Res['ERR']
        try:
            logger.debug(f'Try to click text element {text}')
            ui = self.d.get_ui_by_attr(text=text)
            if ui is not None:
                ui.click()
                res = Res['OK']
                logger.debug(f'Click text element {text} success')
            else:
                logger.debug(f'Not found expect element {text}')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res
    
    def FindElementByXpath(self, xpath:str):
        res = Res['ERR']
        try:
            logger.debug(f'Try to find Xpath element {xpath}')
            ui = self.d.get_ui_by_xpath(xpath=xpath)
            if ui is not None:
                res = Res['OK']
                logger.debug(f'Found expect Xpath {xpath}')
            else:
                logger.debug(f'Not found expect Xpath {xpath}')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res

    def ClickElementByXpath(self, xpath:str):
        res = Res['ERR']
        try:
            logger.debug(f'Try to click Xpath element {xpath}')
            ui = self.d.get_ui_by_xpath(xpath=xpath)
            if ui is not None:
                ui.click()
                res = Res['OK']
                logger.debug(f'Click Xpath element {xpath} success')
            else:
                logger.debug(f'Not found expect Xpath {xpath}')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res

    def ClickByPoint(self, x, y):
        res = Res['ERR']
        try:
            logger.debug(f'Try to click point x={x}, y={y}')
            self.d.adbext.click(x=x, y=y)
            res = Res['OK']
            logger.debug(f'Click point x={x}, y={y} success')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res

    def Swipe(self, start_x, start_y, end_x, end_y, duration):
        res = Res['ERR']
        try:
            logger.debug(f'Try to swipe from {start_x},{start_y} to {end_x},{end_y} in {duration}s')
            start_x, start_y, end_x, end_y, duration = int(start_x), int(start_y), int(end_x), int(end_y), int(duration)
            self.d.adbext.swipe(start_x=start_x,start_y=start_y,end_x=end_x,end_y=end_y,duration=duration)
            res = Res['OK']
            logger.debug(f'Swipe from {start_x},{start_y} to {end_x},{end_y} in {duration}s success')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res
    
    def InputText(self, text:str):
        res = Res['ERR']
        try:
            logger.debug(f'Try to input text {text}')
            self.d.adbext.input(text=text)
            res = Res['OK']
            logger.debug(f'Input text {text} success')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res
    
    def BackHome(self):
        res = Res['ERR']
        try:
            logger.debug(f'Try to back home screen')
            self.d.adbext.home()
            res = Res['OK']
            logger.debug(f'Back home screen success')
        except Exception as e:
            if isinstance(e, NameError):
                logger.debug("Caught a NameError, adb device is not in normal")
            else:
                logger.debug(f"Caught an exception: {e}")
            res = Res['EXCEPTION']
        return res
