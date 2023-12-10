# coding=utf-8
from .adbgetui import GetUI
from .adbutil import Util
from .adbext import AdbExt

class Device(GetUI):
    def __init__(self, sn=None):
        self.util = Util(sn)
        self.adbext = AdbExt(self.util)
        GetUI.__init__(self, self.adbext)
