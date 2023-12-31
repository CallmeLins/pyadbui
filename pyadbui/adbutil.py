# coding=utf-8
import re
import sys
import subprocess
import logging
import platform
import time
import traceback

from func_timeout import func_timeout, FunctionTimedOut


class Util(object):
    def __init__(self, sn):
        self.is_win = 'window' in platform.system().lower()
        self.is_wsl = 'linux' in platform.system().lower() and 'microsoft' in platform.release().lower()  # judge current env
        self.is_py2 = sys.version_info < (3, 0)
        self.sn = sn
        self.adb_path = None
        self.debug = False

    @staticmethod
    def __get_cmd_process(arg):
        logging.debug(arg)
        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # output std and err info
        return p

    @staticmethod
    def __get_cmd_out(process):
        out, err = process.communicate()
        if err.strip():
            logging.error('command {} have err output:\n{}'.format(process.args, err))

        return out

    @staticmethod
    def __run_cmd(arg, is_wait=True, encoding='utf-8'):
        p = Util.__get_cmd_process(arg)
        if is_wait:
            out, err = p.communicate()
        else:
            return p  # if not wait return

        if err:
            logging.error('err: {}, arg: {}'.format(err.strip(), arg))

        if encoding:
            out = out.decode(encoding)
            err = err.decode(encoding)

        try:
            logging.debug('out[: 100]: {}'.format(out[: 100].strip()))
        except Exception as e:
            error_str = traceback.format_exc().strip()
            logging.debug('out log error: {}'.format(error_str))

        p.kill()
        return out, err

    @staticmethod
    def cmd(arg, timeout=30, is_wait=True, encoding='utf-8'):
        """
        execute command return output
        :param arg:
        :param timeout:
        :param is_wait:
        :param encoding:
        :return:
        """
        try:
            return func_timeout(timeout, Util.__run_cmd, args=(arg, is_wait, encoding))
        except FunctionTimedOut:
            print('execute command timeout {}s: {}'.format(timeout, arg))

    def adb(self, arg, timeout=30, encoding='utf-8'):
        self.adb_path = self.adb_path if self.adb_path and self.adb_path != 'adb' else 'adb'

        if not self.sn:
            self.sn = self.get_first_sn()

        arg = '{} -s {} {}'.format(self.adb_path, self.sn, arg)
        for index in range(3):
            result = self.cmd(arg, timeout, encoding=encoding)

            if result is not None and len(result) == 2:
                out, err = result
            else:
                logging.error('execute command return have err: {}'.format(result))
                continue

            if err:  # err handle
                if isinstance(err, bytes):
                    err = err.decode('utf-8')

                # devices connect err handle
                is_device_not_found = 'device' in err and 'not found' in err
                is_device_offline = 'device offline' in err
                if is_device_not_found or is_device_offline:
                    if index == 2:
                        raise NameError('device unavailable: {}'.format(self.sn))
                    self.connect_sn()  # try reconnect device

                else:  # just handle part err
                    return out
            else:  # no error, return result
                return out
        assert False, 'adb run error: {}'.format(arg)

    def shell(self, arg, timeout=30, encoding='utf-8'):
        arg = 'shell {}'.format(arg)
        return self.adb(arg, timeout, encoding=encoding)

    def connect_sn(self):
        if self.sn.count('.') != 3:
            return  # not online devices no handle
        self.cmd('adb disconnect {}'.format(self.sn))  # first disconnect except it is offline
        time.sleep(1)  
        self.cmd('adb connect {}'.format(self.sn))
        time.sleep(1)  # connect it again

        info = self.get_sn_info()
        logging.info('available devices is: {}'.format(info))

    def get_first_sn(self):
        sn_info = self.get_sn_info()
        for sn in sn_info:
            if sn_info[sn] == 'device':
                return sn
        raise NameError('no available devices: {}'.format(sn_info))

    def get_sn_info(self):
        sn_info = {}
        out, err = self.cmd('adb devices')
        lines = re.split(r'[\r\n]+', out.strip())
        for line in lines[1:]:
            if not line.strip():
                continue
            sn, status = re.split(r'\s+', line, maxsplit=1)
            sn_info[sn] = status
        return sn_info
