#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bejond.basic import conn
from bejond.basic.util.static_string import UNDERLINE

stock_hist_index_array = ['code_1_date_-1']
stock_ma_head_up_index_array = ['code_1_date_1'] # 这里date是str，因此是升序


def collection_key_to_tup_array(index_name):
    """
    将mongodb中collection的index转为python collection可读的index的keys。
    比如将'code_1_date_-1'转为[('code', 1), ('date', -1)]
    :param index_name:
    :return: index
    """
    print("original index_name: " + str(index_name))
    params = index_name.split(UNDERLINE) # ['code', '1', 'date', '-1']
    keys = []
    for i in range(len(params)):
        if i % 2 == 0:
            sub = (params[i], int(params[i+1]))
            print(str(sub))
            keys.append(sub)
    print("index: " + str(keys))
    return keys

def create_indexes(collection, index_name_array):
    stock_hist_indexes = collection.index_information()
    indexes = stock_hist_indexes.keys()
    for index_name in index_name_array:
        if index_name not in indexes:
            collection.create_index(collection_key_to_tup_array(index_name), name=index_name)
            print('created new index: ' + index_name)
        # if stock_hist_index[1] not in indexes:
        #     collection_code.create_index([('code', 1)], name = stock_hist_index[1])
        #     print 'created new index: ' + stock_hist_index[1]
