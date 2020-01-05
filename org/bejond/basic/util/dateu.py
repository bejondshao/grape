# !/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import time

import tushare.util.dateu as dateu

from bejond.basic import const

date_format = '%Y-%m-%d'
datetime_format = '%Y-%m-%d %H:%M:%S'


def now():
    """
    获取当前时间。例如：2019-05-19 17:56:18.575693
    :return:
    """
    return datetime.datetime.now()


def to_str(date_, format=date_format):
    """
    将date转为指定格式的str
    :param date_:
    :param format:
    :return:
    """
    return date_.strftime(format)


def get_today_str():
    """
    获取今天日期字符串，不包括时间，返回日期字符串，例如2019-05-19
    :return:
    """
    return time.strftime(date_format)


def get_today():
    """
    获取今天日期，不包括时间，返回日期，例如2019-05-19 00:00:00
    :return:
    """
    return datetime.datetime.strptime(get_today_str(), date_format)


def get_today_time(hours=0):
    """
    备用方法
    获取今天的某个小时的时间，不包含分钟和秒，24小时。例如2019-05-19 13:00:00
    :param hours:
    :return:
    """
    return get_today() + datetime.timedelta(hours=hours)


def get_now_time():
    """
    返回此刻的时间，包含时分秒，格式为2019-05-19 13:20:10
    :return:
    """
    return now().strftime(datetime_format)


def get_close_time():
    """
    获取今天收盘时间，就是今天的下午3点。有可能今天并非交易日，但不影响返回。例如2019-05-19 15:00:00
    :return:
    """
    return get_today_time(15)


def get_previous_date_str(delta=1):
    """
    获取上一个日期str
    :param delta:
    :return:
    """
    previous = now() + datetime.timedelta(days=-delta)
    return previous.strftime(date_format)


def get_previous_date(date_=get_today(), delta=1):
    """
    获取上一个日期
    :param date_: 起始日期，默认为今天
    :param delta: 向前找的日期天数
    :return:
    """
    previous = date_ + datetime.timedelta(days=-delta)
    return previous


def get_latest_trade_date_str(trade_date=None):
    """
    获取上一个交易日str，用于判断是否已经获取过最新历史，节省时间
    '2020-01-03'
    :return:
    """
    if trade_date is None:
        trade_date = get_today()
    while is_weekend_or_holiday(trade_date):
        trade_date = get_previous_date(trade_date)
    return trade_date.strftime(date_format)


def get_next_date_str(date_str):
    date = datetime.datetime.strptime(date_str, date_format)
    date += datetime.timedelta(days=1)

    return date.strftime(date_format)


def get_next_trade_date_str(date_str):
    date = datetime.datetime.strptime(date_str, date_format)
    date += datetime.timedelta(days=1)

    while dateu.is_holiday(date.strftime(date_format)):
        date += datetime.timedelta(days=1)

    return date.strftime(date_format)


def get_next_trade_date(date_str):
    """
            根据传入的字符串日期，获取下一个交易日，返回日期
    """
    date = datetime.datetime.strptime(date_str, date_format)
    date += datetime.timedelta(days=1)

    while dateu.is_holiday(date.strftime(date_format)):
        date += datetime.timedelta(days=1)

    return date


def is_weekday_str(date_str):
    date_ = datetime.datetime.strptime(date_str, date_format)

    return is_weekday(date_)


def is_weekday(date_):
    week_number = datetime.datetime.weekday(date_)

    return week_number <= 4


def is_weekend_or_holiday_str(date_str):
    date_ = datetime.datetime.strptime(date_str, date_format)

    return is_weekend_or_holiday(date_)


def is_weekend_or_holiday(date_=None):
    if date_ is None:
        date_ = get_today()
    date_str = date_.strftime(date_format)
    # print(date_str)
    if not is_weekday(date_) or date_str in const.HOLIDAY_2020:
        return True

    return False


def is_trade_date(date_):
    return not is_weekend_or_holiday(date_)


def is_trade_date_str(date_str):
    return not is_weekend_or_holiday_str(date_str)


def date_delta(date_str1, date_str2):
    """
    根据先后日期，计算日期差距
    :param date_str1:
    :param date_str2:
    :return: 差距几天，int
    """
    date1 = datetime.datetime.strptime(date_str1, date_format)
    date2 = datetime.datetime.strptime(date_str2, date_format)
    return (date2 - date1).days


def get_year():
    return now().year


def calculate_delta(start, end):
    """
    计算程序执行耗时
    :param start: 初始时间
    :param end: 结束时间
    :return:
    """
    seconds = int((end - start).total_seconds())
    minutes = int(seconds / 60)
    if minutes > 0:
        seconds = seconds - minutes * 60
        print("finished in: {m}m {s}s.".format(m=minutes, s=seconds))
    else:
        print("finished in: {s}s.".format(s=seconds))
