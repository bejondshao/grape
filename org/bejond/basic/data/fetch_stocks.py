# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import tushare
import json
import bejond.basic.persistence
import bejond.basic.util.timing
from bejond.basic import const
from bejond.basic.data.ma import mas
from bejond.basic.util import dateu


def save_stock_basics(collection):
    """

    :param collection: 存储的collection名
    :return:
    """
    df_stock_basics = tushare.get_stock_basics()
    df_stock_basics.rename(columns={'esp': 'eps'}, inplace=True)  # 重命名列esp改为eps
    df_stock_basics = df_stock_basics.reset_index() # 将code(string)移到列中
    # 删除stock_basics列表，更新股票信息
    bejond.basic.persistence.database.drop_collection(collection)
    stock_basics = bejond.basic.persistence.database[collection]

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

    start = time.time()
    print(start)
    codes = save_stock_basics(const.STOCK_BASICS)

    # persistence.database.drop_collection('stock_hist')
    collection = bejond.basic.persistence.database.get_collection(const.STOCK_HIST)
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
        last_date = get_last_date(code, collection)
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

            df_hist_data = mas(collection, code, const.DAYS_ARRAY, df_hist_data)

            collection.insert(json.loads(df_hist_data.to_json(orient='records')))
        i += 1
    end = time.time()
    print("Time: " + str(end - start))


save_stock_hist(checks=['000800', '000801'])
