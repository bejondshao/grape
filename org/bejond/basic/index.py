# !/usr/bin/python
# -*- coding: UTF-8 -*-
from bejond.basic import persistence, const

stock_hist_index = ['code_1_date_-1']


def create_indexes():
    collection_code = persistence.database.get_collection(const.STOCK_HIST)

    stock_hist_indexes = collection_code.index_information()
    indexes = stock_hist_indexes.keys()
    if stock_hist_index[0] not in indexes:
        collection_code.create_index([('code', 1), ('date', -1)], name = stock_hist_index[0])
        print 'created new index: ' + stock_hist_index[0]
    # if stock_hist_index[1] not in indexes:
    #     collection_code.create_index([('code', 1)], name = stock_hist_index[1])
    #     print 'created new index: ' + stock_hist_index[1]


create_indexes()
