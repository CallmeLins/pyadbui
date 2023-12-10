# coding=utf-8
import unittest
from pyadbui.adbutil import Util
from pyadbui.adbext import AdbExt
from unittest.mock import MagicMock


class TestAdbExt(unittest.TestCase):
    def setUp(self):
        self.sn = '123abc'
        self.util = Util(self.sn)
        self.util.cmd = MagicMock()
        self.util.cmd.return_value = ''
        self.adbext = AdbExt(self.util)

    def tearDown(self):
        pass

    def test_dump(self):
        self.util.cmd.side_effect = NameError('dump xml fail!')
        self.adbext.dump()
        print(self.util.cmd.call_args_list)

