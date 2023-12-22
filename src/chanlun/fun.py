import logging
import time
import pathlib

import pytz
from functools import wraps

from chanlun.cl_interface import *
from chanlun.config import get_data_path

# 统一时区
__tz = pytz.timezone("Asia/Shanghai")


def get_logger(filename=None, level=logging.INFO) -> logging.Logger:
    """
    获取一个日志记录的对象
    """
    log_path = get_data_path() / "logs"
    if log_path.is_dir() is False:
        log_path.mkdir(parents=True)
    logger = logging.getLogger(f"{filename}")
    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s")
    stream_handler = logging.StreamHandler()

    # 判断之前的handle 是否存在，不存在添加
    stream_exists = False
    file_exists = False
    for _h in logger.handlers:
        if isinstance(_h, logging.StreamHandler):
            stream_exists = True
        if isinstance(_h, logging.FileHandler):
            file_exists = True
    if stream_exists is False:
        logger.addHandler(stream_handler)

    if filename and file_exists is False:
        file_handler = logging.FileHandler(
            filename=str(log_path / filename), encoding="utf-8"
        )
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger


def singleton(cls):
    instance = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return wrapper


def timeint_to_str(_t, _format="%Y-%m-%d %H:%M:%S", tz=__tz):
    """
    时间戳转字符串
    :param _t:
    :param _format:
    :return:
    """
    time_arr = time.localtime(int(_t))
    return time.strftime(_format, time_arr)


def timeint_to_datetime(_t, _format="%Y-%m-%d %H:%M:%S", tz=__tz):
    """
    时间戳转日期
    :param _t:
    :param _format:
    :return:
    """
    time_arr = time.localtime(int(_t))
    return str_to_datetime(time.strftime(_format, time_arr), _format, tz=tz)


def str_to_timeint(_t, _format="%Y-%m-%d %H:%M:%S"):
    """
    字符串转时间戳
    :param _t:
    :param _format:
    :return:
    """
    return int(time.mktime(time.strptime(_t, _format)))


def str_to_datetime(_s, _format="%Y-%m-%d %H:%M:%S", tz=__tz):
    """
    字符串转datetime类型
    :param _s:
    :param _format:
    :return:
    """
    return datetime.datetime.strptime(_s, _format).astimezone(tz)


def datetime_to_str(_dt: datetime.datetime, _format="%Y-%m-%d %H:%M:%S"):
    """
    datetime转字符串
    :param _dt:
    :param _format:
    :return:
    """
    return _dt.strftime(_format)


def datetime_to_int(_dt: datetime.datetime):
    """
    datetime转时间戳
    :param _dt:
    :return:
    """
    return int(_dt.timestamp())


def str_add_seconds_to_str(_s, _seconds, _format="%Y-%m-%d %H:%M:%S"):
    """
    字符串日期时间，加上秒数，在返回新的字符串日期
    """
    _time = int(time.mktime(time.strptime(_s, _format)))
    _time += _seconds
    _time = time.localtime(int(_time))
    return time.strftime(_format, _time)


def now_dt():
    """
    返回当前日期字符串
    """
    return datetime_to_str(datetime.datetime.now(tz=__tz))


if __name__ == "__main__":
    nowdt = now_dt()
    print(nowdt)

    print(str_to_datetime(nowdt))

    dtint = str_to_timeint(nowdt)
    print(dtint)

    print(timeint_to_datetime(dtint))

    print(timeint_to_str(dtint))
