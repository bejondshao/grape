#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pandas

from bejond.basic import conn, const
from bejond.basic.datamodel.one_day import OneDay, Slope
from bejond.basic.datamodel.two_days import TwoDays
from bejond.basic.util import dateu


def find_head_up(code=None, start=None, end=None, pb=None, pe=None, delta=60):
    """
    根据ma_60计算趋势，可以将计算结果代码，组合成url直接在某个网站打开。
    :param code:
    :param start:
    :param end:
    :param pb:
    :param pe:
    :param delta:
    :return:
    """
    codes = conn.collection_stock_basics.find({'timeToMarket': {'$lt': 20170101}, 'pb': {'$lt': 4}, 'pe': {'$lt': 22, '$gt': 0}}, {'code': 1, '_id': 0})  # codes为Cursor {'code': 'xxxxxx'}

    code_date_list = []
    for code_cursor in codes:  # 分析每只股票
        code = code_cursor['code']
        #code = '600741'
        histories = pandas.DataFrame(list(conn.collection_stock_hist.find(
            {'code': code, 'ma_60': {'$gt': 0}}).sort([('date', -1)]).limit(delta)))
        histories = histories[::-1]  # reverse所查询的结果，将早的日期放到前面
        first = None
        second = None

        days_list = []
        for history in histories.itertuples():  # 根据股票历史计算没两天股票斜率，并放到list中
            date = getattr(history, 'date')
            close = getattr(history, 'close')
            ma_60 = getattr(history, 'ma_60')
            if first is None:
                first = OneDay(code, date, close, ma_60)
                continue

            second = OneDay(code, date, close, ma_60)
            second.slope = second.get_slope(first)
            days_list.append(second)
            first = second

        # for history in histories:  # 根据股票的历史，组合成前后两天为一组的数据模型
        #     date = history['date']
        #     close = history['close']
        #     ma_60 = history['ma_60']
        #     if first is None:
        #         first = OneDay(date, close, ma_60)
        #         continue
        #
        #     second = OneDay(date, close, ma_60)
        #     two_days = TwoDays(first, second)
        #     two_days_list.append(two_days)
        #     first = second

        if len(days_list) > 0:  # 根据斜率变化，判断股票走势
            if end is None:
                end = dateu.get_today()
            if start is None:
                start = dateu.get_previous_date_str(delta/8)
            day_first = None
            for day in days_list:
                if day_first is None:
                    day_first = day
                    continue
                if day_first.slope < 0 <= day.slope and start < day.date < end and day.close > day.ma_60:
                    print(day.code + ": " + day.date)
                    code_date_list.append(day)
                    break
                # elif day_first.slope > 0:
                #     break
                else:
                    day_first = day

    return code_date_list

"""
    执行完fetch_stocks.py的save_stock_hist()和repair_mas()后，执行find_head_up()，查找开启抬头的股票。
    有个小问题，就是有时候会选出涨到顶峰的股票。
"""

list1 = find_head_up()
print(len(list1))