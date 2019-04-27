# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import tushare
import json
import bejond.basic.util.timing
from bejond.basic import const, conn
from bejond.basic.data import ma
from bejond.basic.data.ma import mas
from bejond.basic.util import dateu


def save_stock_basics(collection_name):
    """

    :param collection: 存储的collection名
    :return:
    """
    df_stock_basics = tushare.get_stock_basics()
    df_stock_basics.rename(columns={'esp': 'eps'}, inplace=True)  # 重命名列esp改为eps
    df_stock_basics = df_stock_basics.reset_index()  # 将code(string)移到列中
    # 删除stock_basics列表，更新股票信息
    conn.database.drop_collection(collection_name)
    stock_basics = conn.database[collection_name]

    stock_basics.insert(json.loads(df_stock_basics.to_json(orient='records')))
    return df_stock_basics['code']


def get_last_date(code, collection_code):
    last_date = collection_code.find(
        {'code': code}
    ).sort([('date', -1)]).limit(1)

    if last_date.count() > 0:
        return last_date[0]['date']

    return None


def save_stock_hist(checks=None):
    """
    更新股票历史，建议每日收盘后运行。因为收盘前运行当日数据会有误
    :param checks: 临时更新某些股票的历史，节省时间。checks=None时更新所有股票历史
    :return:
    """

    codes = save_stock_basics(conn.stock_basics)

    # persistence.database.drop_collection('stock_hist')

    i = 1
    if checks is not None:
        codes = checks
    for code in codes:
        last_date = None
        # persistence.database.drop_collection(code)
        #if collection_code is not None:
        # last_result = collection_code.find({}).sort('date', -1).limit(1)
        #    last_result = collection_code.find({}).sort({'date': -1}).limit(1)

        #df_hist_data = None
        print(i)
        print(code)
        last_date = get_last_date(code, conn.collection_stock_hist)
        print('last_date ' + str(last_date))

        if last_date is None: # 如果数据库未找到上一次存储的日期，说明是新股票
            df_hist_data = tushare.get_hist_data(code)
        else: # 如果找到上次存储的日期
            # next_trade_date = dateu.get_next_trade_date(last_date) # 获取下个交易日，is_holiday读取csv速度太慢，放弃
            # if next_trade_date < datetime.now():
            df_hist_data = tushare.get_hist_data(code, dateu.get_next_date_str(last_date))
        if df_hist_data is not None and len(df_hist_data.index) > 0:
            df_hist_data = df_hist_data.iloc[::-1] # get_hist_data的返回结果是降序的，reverse
            print(df_hist_data.index)

            '''
            注意：如果调用tushare.get_k_data，index是自增数字，date是一列。
            tushare.get_hist_data返回date是index。
            由于get_k_data在设定start时无法返回当天数据，所以弃用
            另外，如果在收盘前调用查询历史接口，当天返回的数据中，close为调用时的股票价格，不正确。应该做处理
            '''
            df_hist_data = df_hist_data.reset_index()  # 将date(string)移到列中。
            df_hist_data['code'] = code

            df_hist_data = mas(conn.collection_stock_hist, code, const.DAYS_ARRAY, df_hist_data)

            conn.collection_stock_hist.insert(json.loads(df_hist_data.to_json(orient='records')))
        i += 1


def repair_mas():
    """
    只是用于修复之前获取的数据，并未求ma_30和ma_60。新数据库不会用到该函数。除非要增加新的平均线
    :return:
    """
    codes = save_stock_basics(conn.stock_basics)
    i = 1
    for code in codes:
        print(i)
        print("Repairing mas. Code: " + code)
        ma.repair_mas(conn.collection_stock_hist, code, const.DAYS_ARRAY)
        i += 1


"""
   1. 先执行save_stock_hist() （注释repare_mas()），获取股票历史信息
   2. 再执行repair_mas()（注释save_stock_hist()），修复ma_30和ma_60的值
"""
# save_stock_hist()
repair_mas()