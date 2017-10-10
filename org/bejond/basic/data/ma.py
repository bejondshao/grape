# !/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division

from collections import deque

import pandas

from bejond.basic.data.data_total import DataTotal
from org.bejond.basic import persistence
from bejond.basic import const


def ma(days):
    collection_code = persistence.database.get_collection(const.STOCK_HIST)
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


def mas(collection, code, days_array, df_hist_data):
    """

    :param collection: 历史数据库
    :param code: 股票代码
    :param days_array: 要求的均线日期数组，比如[5, 10, 20, 30, 60]
    :param df_hist_data: 每日交易信息, DataFrame
    :return: 增加均线后的df_hist_data
    """
    for days in days_array:
        # df['ma_' + str(ma)] = pd.rolling_mean(df['close'], ma)
        previous_data = fetch_previous_data(collection, code, days)
        count = len(previous_data.index) # 记录从数据库获取了多少条数据，用于后续去掉
        df_hist_data = previous_data.append(df_hist_data)
        df_hist_data['ma_' + str(days)] = pandas.Series(df_hist_data['close']).rolling(window=days).mean()
        df_hist_data = df_hist_data.iloc[count:]
        # fix_mas(days, df_hist_data)
    return df_hist_data


def fetch_previous_data(collection, code, days):
    """

    :param collection: STOCK_HIST的collection
    :param code: 股票代码
    :param days: 平均数的天数
    :return: 获取的days-1天的历史，DataFrame
    """
    days_1 = days - 1
    stock_hist = collection.find({'code': code}, {'close': 1, 'date': 1, '_id': 0}).sort([('date', -1)]).limit(days_1)

    df = pandas.DataFrame(list(stock_hist), columns=['close', 'date'])
    return df[::-1] # reverse所查询的结果，将早的日期放到前面


def fix_mas(days, df_hist_data):
    """

    :param days: 日线天数
    :param df_hist_data: 增加均线后的每日交易信息, DataFrame。针对数据不全而导致ma_x为NaN时，需要读取数据库数据来计算均线
    :return: 增加均线后的df_hist_data
    """
    collection_code = persistence.database.get_collection(const.STOCK_HIST)
    days_1 = days - 1
    stock_hist = collection_code.find({'code': df_hist_data['code']}, {'close': 1, '_id': 0}).sort([('date', 1)]).limit(days_1)
    data_total = DataTotal(stock_hist)

    for df_hist_data_each in df_hist_data:
        if len(data_total.data) == days_1:
            data_total.append(df_hist_data_each['close']) # ???
            ma = data_total.total / days


