# coding=utf-8
import subprocess
from lxml import etree
from pyadbui import Device
from pyadbui import Util
import logging
logging.basicConfig(level=logging.DEBUG)

d = Device()

ui = d.get_uis_by_ocr('')
print(ui)
