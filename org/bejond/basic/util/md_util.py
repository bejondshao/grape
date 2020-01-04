# !/usr/bin/python
# -*- coding: UTF-8 -*-
import webbrowser

from bejond.basic.const import MD_URL
from bejond.basic.util.static_string import SPAN, NECK, NEWLINE


def to_table_head(cls):
    """
    将对象的属性转为markdown表头
    :param cls:
    :return:
    """
    to_head = neck = SPAN
    for attribute in cls.attributes():
        to_head += attribute + SPAN
        neck += NECK + SPAN
    to_head += NEWLINE + neck + NEWLINE
    return to_head

def to_table_row(cls):
    """
    将对象转换为"|601211|国泰君安|2019-12-30|证券|上海|18.68|"形式，输出为markdown的table一行
    :return:
    """
    to_string = SPAN
    for attribute in cls.attributes():
        to_string += cls.__getattribute__(attribute) + SPAN
    to_string += NEWLINE
    return to_string


def to_url_open(stock_url, filtered_stock):
    """
    将代码转为
    :param cls: StockUrl对象
    :return: 转为markdown格式的雪球url
    """
    webbrowser.open(stock_url.xueqiu_url)
    webbrowser.open(stock_url.lixinger_url)
    url = MD_URL.format(code=stock_url.code, url=stock_url.xueqiu_url)
    # 将过滤的股票的code转为url形式，输出到文件中
    filtered_stock.code = url
    return url