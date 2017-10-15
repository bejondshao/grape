# !/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division

from bejond.basic.data.data_total import DataTotal
from org.bejond.basic import conn
from bejond.basic import const
from collections import deque

import pandas


def ma(days):
    codes = list(conn.collection_stock_basics.find({}, {'code': 1, '_id': 0}))
    for code in codes:
        print(code['code'])

    for code in codes:
        stock_hist = conn.collection_stock_hist.find({'code': code['code']}).sort([('date', 1)])
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
    return df[::-1]  # reverse所查询的结果，将早的日期放到前面


def fix_mas(days, df_hist_data):
    """

    :param days: 日线天数
    :param df_hist_data: 增加均线后的每日交易信息, DataFrame。针对数据不全而导致ma_x为NaN时，需要读取数据库数据来计算均线
    :return: 增加均线后的df_hist_data
    """
    days_1 = days - 1
    stock_hist = conn.collection_stock_hist.find({'code': df_hist_data['code']}, {'close': 1, '_id': 0}).sort([('date', 1)]).limit(days_1)
    data_total = DataTotal(stock_hist)

    for df_hist_data_each in df_hist_data:
        if len(data_total.data) == days_1:
            data_total.append(df_hist_data_each['close']) # ???
            ma = data_total.total / days


def repair_mas(collection, code, days_array):
    """

    :param collection: 历史数据库
    :param code: 股票代码
    :param days_array: 要求的均线日期数组，比如[5, 10, 20, 30, 60]
    :return: 修复后的数据
    """
    stock_hist = collection.find(
        {'code': code},
        {'_id': 1,
         'code': 1,
         'date': 1,
         'close': 1}
    ).sort([('date', 1)])

    df = pandas.DataFrame(list(stock_hist), columns=const.STOCK_HIST_SIMPLE_COLUMNS)
    df.rename(columns={const.STOCK_HIST_MONGO_ID: const.PANDAS_DATA_FRAME_ID}, inplace=True)  # 重命名列_id改为id
    for days in days_array:
        df['ma_' + str(days)] = pandas.Series(df['close']).rolling(window=days).mean()

    for row in df.itertuples():
        collection.update(
            {
                const.STOCK_HIST_MONGO_ID: getattr(row, const.PANDAS_DATA_FRAME_ID)  # id
            },
            {
                '$set':
                    {
                        'ma_30': getattr(row, 'ma_30'),  # ma_30
                        'ma_60': getattr(row, 'ma_60')  # ma_60
                    }
            }
        )