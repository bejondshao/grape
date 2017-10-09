# !/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division

from collections import deque

import pandas

from bejond.basic.data.data_total import DataTotal
from org.bejond.basic import persistence
from bejond.basic import const


def ma(days):
    collection_code = persistence.database.get_collection(const.STOCK_K_HIST)
    codes = list(persistence.database.get_collection(const.STOCK_BASICS).find({}, {'code': 1, '_id': 0}))
    for code in codes:
        print(code['code'])

    for code in codes:
        code = {'code':'000800'}
        stock_hist = collection_code.find({'code': code['code']}).sort([('date', 1)])
        if stock_hist.count() >= days:
            values = deque(maxlen=days)
            for i in range(0, days):
                values.append(stock_hist[i]['close'])
            total = 0.0
            for value in values:
                total += value
            ma = total / days
            print(ma)
        break
        # for stock_hist_code in stock_hist:
        #     print stock_hist_code['date']


def mas(days_array, df_k_data):
    """

    :param days_array: 要求的均线日期数组，比如[5, 10, 20, 30, 60]
    :param df_k_data: 每日交易信息, DataFrame
    :return: 增加均线后的df_k_data
    """
    for days in days_array:
        # df['ma_' + str(ma)] = pd.rolling_mean(df['close'], ma)
        df_k_data['ma_' + str(days)] = pandas.Series(df_k_data['close']).rolling(window=days).mean()
        fix_mas(days, df_k_data)# ???


def fix_mas(days, df_k_data):
    """

    :param days: 日线天数
    :param df_k_data: 增加均线后的每日交易信息, DataFrame。针对数据不全而导致ma_x为NaN时，需要读取数据库数据来计算均线
    :return: 增加均线后的df_k_data
    """
    collection_code = persistence.database.get_collection(const.STOCK_K_HIST)
    days_1 = days - 1
    stock_hist = collection_code.find({'code': df_k_data['code']}, {'close': 1, '_id': 0}).sort([('date', 1)]).limit(days_1)
    data_total = DataTotal(stock_hist)

    for df_k_data_each in df_k_data:
        if len(data_total.data) == days_1:
            data_total.append(df_k_data_each['close']) # ???
            ma = data_total.total / days



ma(days=60)
