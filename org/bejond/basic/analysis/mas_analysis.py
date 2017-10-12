# !/usr/bin/python
# -*- coding: UTF-8 -*-

from bejond.basic import conn, const


def find_head_up():
    codes = conn.collection_stock_basics.find({}, {'code': 1, '_id': 0})
    for code in codes:
        histories = list(conn.collection_stock_hist.find({'code': code}).sort([('date', 1)]).limit(60))

        for history in histories:
            date = history['date']
            ma_60 = history['ma_60']