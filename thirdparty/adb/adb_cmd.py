# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-29'
from common.decorator import memoize
import platform, psutil, os, shutil, subprocess
import settings
from common.logger import msflogger
import datetime, time


# ps aux | grep proc
def find_process_by(proc: str):
    return set([p.exe() for p in psutil.process_iter(attrs=['name']) if proc == p.info['name']])


# find executable
def find_bin_by(bin_file: str):
    return shutil.which(bin_file) is not None or os.access(bin_file, os.X_OK)


# is file exist
def is_file_exists(file):
    return os.path.isfile(file) or shutil.which(file)


# is dir
def is_dir_exists(dir):
    return os.path.isdir(dir)


@memoize
def _get_cmd_bin():
    adb_path = ''
    try:
        adb_msg = 'not found adb binary'
        if find_bin_by(settings.ADB_BINARY):
            adb_path = settings.ADB_BINARY
        if platform.system() == 'Windows':
            if find_bin_by('adb.exe'):
                adb_path = 'adb.exe'
        else:
            if find_bin_by('adb'):
                adb_path = 'adb'

        return adb_path

    except Exception as e:
        if not adb_path:
            msflogger.warning(f'Exception: Cannot find adb executable! {adb_msg} {str(e)}. ')
    finally:
        if adb_path:
            os.environ['MOBSF_ADB'] = adb_path
        else:
            os.environ['MOBSF_ADB'] = ''
            msflogger.warning('not found adb executable! %s. ', adb_msg)
    return adb_path


def cmd_execute(cmd: str, device_id: str, timeout: int = 5):
    '''
    Execute ADB Commands.
    :param cmd:
    :param device_id:
    :param timeout:
    :return:
    '''
    if cmd:
        if device_id:
            args = [_get_cmd_bin(), '-s', device_id]
        else:
            args = [_get_cmd_bin()]
        try:
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
            sub = subprocess.Popen(args + cmd.split(' '),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            while True:
                if sub.poll() is not None:
                    break
                time.sleep(0.1)
                if timeout and end_time <= datetime.datetime.now():
                    sub.kill()
                    return '', 'cmd execute timeout'

            return sub.stdout.read(), sub.stderr.read()
        except Exception as e:
            msflogger.exception(f'Executing ADB Commands. {str(e)}')
    else:
        msflogger.warning(f'cmd execute params error cmd({cmd}) device_id({device_id})')
        return '', 'cmd execute exception'
