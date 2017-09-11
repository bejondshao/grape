# !/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
import json
import persistance
import resource

resource.getrlimit(resource.RLIMIT_FSIZE)

def save_stock_basics(collection):
    """

    :param collection: 存储的collection名
    :return:
    """
    df_stock_basics = ts.get_stock_basics()
    df_stock_basics.rename(columns = {'esp':'eps'}, inplace = True)  # 重命名列esp改为eps
    df_stock_basics = df_stock_basics.reset_index() # 将code(string)移到列中
    persistance.database.drop_collection(collection)
    stock_basics = persistance.database[collection]

    stock_basics.insert(json.loads(df_stock_basics.to_json(orient='records')))
    return df_stock_basics['code']

def save_stock_hist(start=None, end=None):

    codes = save_stock_basics('stock_basics')

    persistance.database.drop_collection('stock_hist')
    collection_code = persistance.database.get_collection('stock_hist')
    for code in codes:
        last_result = None
        persistance.database.drop_collection(code)
        #if collection_code is not None:
        # last_result = collection_code.find({}).sort('date', -1).limit(1)
        #    last_result = collection_code.find({}).sort({'date': -1}).limit(1)

        #df_hist_data = None
        if last_result is None:
            df_hist_data = ts.get_hist_data(code)
        else:
            df_hist_data = ts.get_hist_data(code, last_result.next().date)
        if df_hist_data is not None:
            df_hist_data = df_hist_data.reset_index() # 将date(string)移到列中
            df_hist_data['code'] = code
            collection_code.insert(json.loads(df_hist_data.to_json(orient='records')))


save_stock_hist(start='2017-08-01', end='2017-08-20')