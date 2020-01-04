#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json

import tushare

from bejond.basic import const, conn
from bejond.basic.data import ma
from bejond.basic.data.ma import mas
from bejond.basic.util import dateu


def save_stock_basics(collection_name):
    """
    更新股票列表，删除表重新获取并插入。不用更新的方式是因为股票数目和名称会变化，包括股票的其他属性。既然是每条检查，不如重新获取
    :param collection_name: 存储的collection名
    :return:
    """
    df_stock_basics = tushare.get_stock_basics()
    df_stock_basics.rename(columns={'esp': 'eps'}, inplace=True)  # 重命名列esp改为eps
    df_stock_basics = df_stock_basics.reset_index()  # 将code(string)移到列中
    # 删除stock_basics列表，更新股票信息
    conn.database.drop_collection(collection_name)
    stock_basics = conn.database[collection_name]

    stock_basics.insert_many(json.loads(df_stock_basics.to_json(orient='records')))
    return df_stock_basics['code']


def get_last_date(code, collection_code):
    last_date = collection_code.find(
        {'code': code}
    ).sort([('date', -1)]).limit(1)

    if last_date.count() > 0:
        return last_date[0]['date']

    return None


def is_before_close_time():
    """
    根据当前时间和当天15点收盘时间比较，如果时间在15点之前，则返回True
    :return:
    """
    close_time = dateu.get_close_time()
    return dateu.now() < close_time


def save_stock_hist(checks=None, repair_days=0):
    """
    更新股票历史，建议每日收盘后运行。因为收盘前运行当日数据会有误 TODO, 修改fetch日期，如果今天为交易日并且运行时间在收盘前，则不存储今天的数据
    :param checks: 临时更新某些股票的历史，节省时间。checks=None时更新所有股票历史
    :param repair_days 要修复的天数，默认是0。因为有时候会错误的在交易期间更新数据，而当天所有股票的最高价，最低价，收盘价有可能
    都是错误的，这回影响其他参数的计算。因此需要修复，填入一个数值，会删掉库里的最后n天记录，然后重新获取。
    :return:
    """

    codes = save_stock_basics(conn.stock_basics)

    # persistence.database.drop_collection('stock_hist')

    i = 1
    if checks is not None:
        codes = checks

    # calculate end out of for loop to save time
    end = None
    if is_before_close_time():
        end = dateu.get_previous_date_str(1)
    today_str = dateu.get_today_str()
    for code in codes:
        last_date = None
        # persistence.database.drop_collection(code)
        # if collection_code is not None:
        # last_result = collection_code.find({}).sort('date', -1).limit(1)
        #    last_result = collection_code.find({}).sort({'date': -1}).limit(1)

        # df_hist_data = None
        last_date = get_last_date(code, conn.collection_stock_hist)

        if last_date is None:  # 如果数据库未找到上一次存储的日期，说明是新股票
            df_hist_data = tushare.get_hist_data(code, end=end)
        elif last_date.__eq__(today_str):  # 如果last_date和最近一个交易日（如果今天此时时间不到收盘时间，则是上一个交易日。如果时间是收盘时间后，则是今天）一样，说明获取过，就跳过
            # elif last_date.__eq__(dateu.get_previous_date_str(1)): # 这一行是周六测试用，忽略
            continue
        else:  # 如果找到上次存储的日期且日期不是最近的交易日
            # next_trade_date = dateu.get_next_trade_date(last_date) # 获取下个交易日，is_holiday读取csv速度太慢，放弃
            # if next_trade_date < datetime.now():
            print(i)
            print(code)
            print('last_date ' + str(last_date))
            repeat = True
            while repeat:
                try:
                    df_hist_data = tushare.get_hist_data(code, start=dateu.get_next_date_str(last_date), end=end)
                    repeat = False
                except Exception as e:
                    continue

        if df_hist_data is not None and len(df_hist_data.index) > 0:
            df_hist_data = df_hist_data.iloc[::-1]  # get_hist_data的返回结果是降序的，reverse
            print(df_hist_data.index)

            '''
            注意：如果调用tushare.get_k_data，index是自增数字，date是一列。
            tushare.get_hist_data返回date是index。
            由于get_k_data在设定start时无法返回当天数据，所以弃用
            另外，如果在收盘前调用查询历史接口，当天返回的数据中，close为调用时的股票价格，不正确。应该做处理
            '''
            df_hist_data = df_hist_data.reset_index()  # 将date(string)移到列中。
            df_hist_data['code'] = code

            # 自行计算ma_30和ma_60
            df_hist_data = mas(conn.collection_stock_hist, code, const.DAYS_ARRAY, df_hist_data)

            conn.collection_stock_hist.insert_many(json.loads(df_hist_data.to_json(orient='records')))
        i += 1


def repair_mas():
    """
    只是用于修复之前获取的数据，并未求ma_30和ma_60。新数据库不会用到该函数。除非要增加新的平均线
    :return:
    """
    codes = save_stock_basics(conn.stock_basics)
    i = 1
    collection = conn.collection_stock_hist
    for code in codes:
        ma.repair_mas(collection, code, const.DAYS_ARRAY)
        i += 1


def repair_turnover():
    """
    turnover，换手率，接口文档tushare.get_hist_data()提示是有返回，但是并没有，因此需要自己计算，计算规则是：当日成交量(手) * 100 / (流通股(亿股) * 100000000) * 100%。即 volumn / outstanding / 1000000
    :return: turnover
    """
    codes = save_stock_basics(conn.stock_basics)
    i = 1
    collection = conn.collection_stock_hist
    for code in codes:
        print(i)
