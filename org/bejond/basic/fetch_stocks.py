# !/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
import json
import persistance
from bejond.basic.util import dateu


def save_stock_basics(collection):
    """

    :param collection: 存储的collection名
    :return:
    """
    df_stock_basics = ts.get_stock_basics()
    df_stock_basics.rename(columns = {'esp':'eps'}, inplace = True)  # 重命名列esp改为eps
    df_stock_basics = df_stock_basics.reset_index() # 将code(string)移到列中
    # 删除stock_basics列表，更新股票信息
    persistance.database.drop_collection(collection)
    stock_basics = persistance.database[collection]

    stock_basics.insert(json.loads(df_stock_basics.to_json(orient='records')))
    return df_stock_basics['code']


def get_last_date(code, collection_code):
    last_date = collection_code.find(
        {'code': code}
    ).sort([('date', -1)]).limit(1)

    if last_date.count() > 0:
        return last_date[0]['date']

    return None


def save_stock_hist(start=None, end=None):

    codes = save_stock_basics('stock_basics')

    # persistance.database.drop_collection('stock_hist')
    collection_code = persistance.database.get_collection('stock_hist')
    i = 1
    for code in codes:
        last_date = None
        # persistance.database.drop_collection(code)
        #if collection_code is not None:
        # last_result = collection_code.find({}).sort('date', -1).limit(1)
        #    last_result = collection_code.find({}).sort({'date': -1}).limit(1)

        #df_hist_data = None
        print i
        print code
        last_date = get_last_date(code, collection_code)
        print 'last_date ' + str(last_date)

        if last_date is None: # 如果数据库未找到上一次存储的日期，说明是新股票
            df_hist_data = ts.get_hist_data(code, end)
        else: # 如果找到上次存储的日期
            # next_trade_date = dateu.get_next_trade_date(last_date) # 获取下个交易日，is_holiday读取csv速度太慢，放弃
            # if next_trade_date < datetime.now():
            df_hist_data = ts.get_hist_data(code, dateu.get_next_date_str(last_date), end)
        if df_hist_data is not None and len(df_hist_data.index) > 0:
            print df_hist_data.index
            df_hist_data = df_hist_data.reset_index() # 将date(string)移到列中
            df_hist_data['code'] = code
            collection_code.insert(json.loads(df_hist_data.to_json(orient='records')))
        i += 1


save_stock_hist()
