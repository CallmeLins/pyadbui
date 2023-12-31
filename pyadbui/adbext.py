# coding=utf-8
import os
import re
import time
import base64
import logging
import tempfile


class AdbExt(object):
    def __init__(self, util):
        self.util = util
        self.is_helper_ready = False
        self.width, self.height = None, None
        self.dir_path = os.path.dirname(os.path.abspath(__file__))  # absolute path to the directory where the current file is located
        self.temp_device_dir_path = '/data/local/tmp'

    def init_device_size(self):
        if self.width and self.height:
            return
        out = self.util.shell('wm size')  # out like 'Physical size: 1080x1920'
        out = re.findall(r'\d+', out)
        self.width = int(out[0])
        self.height = int(out[1])

    def dump(self):
        for i in range(5):
            xml_str = self.__dump_xml()
            if xml_str:
                return xml_str
            time.sleep(1)
        raise NameError('dump xml fail!')

    def __dump_xml(self):
        # use helper get xml
        xml_str = self.run_helper_cmd('layout')

        # compression mode
        if not xml_str:
            xml_str = self.util.adb('exec-out uiautomator dump --compressed /dev/tty', encoding='')

        # none compression mode
        if not xml_str:
            xml_str = self.util.adb('exec-out uiautomator dump /dev/tty', encoding='')

        if isinstance(xml_str, bytes):
            xml_str = xml_str.decode('utf-8')

        if 'hierarchy' in xml_str:
            start = xml_str.find('<hierarchy')
            end = xml_str.rfind('>') + 1
            xml_str = xml_str[start: end].strip()
            return xml_str

    def run_helper_cmd(self, cmd):
        """
        execute helper cmd, support dump xml and screenshot
        :param cmd:
        :return:
        """
        if not self.is_helper_ready:
            file_names = self.util.shell('ls {}'.format(self.temp_device_dir_path))
            if 'adbui' not in file_names:
                helper_path = os.path.join(self.dir_path, 'static', 'adbui')
                self.push(helper_path, self.temp_device_dir_path)
            self.is_helper_ready = True
        arg = 'app_process -Djava.class.path=/data/local/tmp/adbui /data/local/tmp com.ysbing.yadb.Main -{}'.format(cmd)
        return self.util.shell(arg)

    def delete_from_device(self, path):
        self.util.shell('rm -rf {}'.format(path))

    def screenshot(self, pc_path=None):
        out = self.run_helper_cmd('screenshot')
        if out and len(out) > 50:
            out = base64.b64decode(out)
        else:  # helper screenshot faild, use screencap screenshot
            logging.warning('helper screenshot faild')
            arg = 'exec-out screencap -p'.format(self.util.sn)
            out = self.util.adb(arg, encoding=None)  # png bytes string

        # save screenshot
        if pc_path:
            if self.util.is_py2:
                pc_path = pc_path.decode('utf-8')
            if os.path.exists(pc_path):  # del pc fail
                os.remove(pc_path)
            with open(pc_path, 'wb') as f:
                f.write(out)
            return pc_path

        return out

    def pull(self, device_path=None, pc_path=None):
        return self.util.adb('pull "{}" "{}"'.format(device_path, pc_path))

    def push(self, pc_path=None, device_path=None):
        return self.util.adb('push "{}" "{}"'.format(pc_path, device_path))

    def click(self, x, y):
        self.util.shell('input tap {} {}'.format(x, y))

    def long_click(self, x, y, duration=''):
        """
        long click
        :param x: x coordinate
        :param y: y coordinate
        :param duration: long click time(ms)
        :return:
        """
        self.util.shell('input touchscreen swipe {} {} {} {} {}'.format(x, y, x, y, duration))

    def start(self, pkg):
        """
        use monkey start a app via package name
        :param pkg:
        :return:
        """
        self.util.shell('monkey -p {} 1'.format(pkg))

    def stop(self, pkg):
        self.util.shell('am force-stop {}'.format(pkg))

    def input(self, text):
        self.util.shell('input text "{}"'.format(text.replace('&', '\&')))

    def back(self, times=1):
        while times:
            self.util.shell('input keyevent 4')
            times -= 1

    def home(self):
        self.util.shell('input keyevent 3')

    def enter(self, times=1):
        while times:
            self.util.shell('input keyevent 66')
            times -= 1

    def swipe(self, e1=None, e2=None, start_x=None, start_y=None, end_x=None, end_y=None, duration=" "):
        """
        swipe event
        usage: swipe(e1, e2)
               swipe(e1, end_x=200, end_y=500)
               swipe(start_x=0.5, start_y=0.5, e2)
        """
        self.init_device_size()
        if e1 is not None:
            start_x = e1[0]
            start_y = e1[1]
        if e2 is not None:
            end_x = e2[0]
            end_y = e2[1]
        if 0 < start_x < 1:
            start_x = start_x * self.width
        if 0 < start_y < 1:
            start_y = start_y * self.height
        if 0 < end_x < 1:
            end_x = end_x * self.width
        if 0 < end_y < 1:
            end_y = end_y * self.height

        self.util.shell('input swipe %s %s %s %s %s' % (str(start_x), str(start_y), str(end_x), str(end_y), str(duration)))

    def clear(self, pkg):
        """
        reset app
        :param pkg:
        :return:
        """
        self.util.shell('pm clear {}'.format(pkg))

    def wake_up(self):
        """
        wakeup screen
        :return:
        """
        self.util.shell('input keyevent KEYCODE_WAKEUP')

    def unlock(self):
        """
        unlock screen
        :return:
        """
        self.util.shell('input keyevent 82')

    def grant(self, pkg, permission):
        """
        give permission via adb shell pm grant [PACKAGE_NAME] android.permission.PACKAGE_USAGE_STATS
        :return:
        """
        self.util.shell('pm grant {} {}'.format(pkg, permission))

    def install(self, apk_path, with_g=True, with_r=False, user=None):
        """
        install package
        :param apk_path:
        :param with_g: -g on some devices, automatic authorization can be granted, with a default of true
        :param with_r: -r overwrite installation, default false
        :param user:
        :return:
        """
        arg = 'install'
        if user:
            arg = arg + ' -user {}'.format(user)
        if with_g:
            arg = arg + ' -g'
        if with_r:
            arg = arg + ' -r'
        self.util.adb('{} "{}"'.format(arg, apk_path), timeout=60 * 5)  

    def uninstall(self, pkg):
        """
        uninstall package
        :param pkg:
        :return:
        """
        self.util.adb('uninstall {}'.format(pkg))

    def get_name(self, remove_blank=False):
        name = self.util.shell('getprop ro.config.marketing_name').strip()
        if not name:
            name = self.util.shell('getprop ro.product.nickname').strip()
        if remove_blank:
            name = name.replace(' ', '')
        return name

    def switch_user(self, user_id, wait_time=5):
        self.util.shell('am switch-user {}'.format(user_id))
        time.sleep(wait_time)

    def list_packages(self, system=False):
        """
        return package lsit have been installed
        :param system:  incloud system package or not
        :return:
        """
        with_system = '' if system else '-3'
        return self.util.shell('pm list packages {}'.format(with_system))
