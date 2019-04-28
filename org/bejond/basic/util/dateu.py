# !/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import time

import tushare.util.dateu as dateu

from bejond.basic import const

date_format = '%Y-%m-%d'


def get_today():
    return time.strftime(date_format)


def get_previous_date_str(delta):
    now = datetime.datetime.now()
    previous = now + datetime.timedelta(days=-delta)
    return previous.strftime(date_format)


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


def is_weekend_or_holiday(date_):
    date_str = date_.strftime(date_format)
    print(date_str)
    if not is_weekday(date_) or date_str in const.HOLIDAY_2016 or date_str in const.HOLIDAY_2017:
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
