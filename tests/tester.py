# !/usr/bin/python
# -*- coding: UTF-8 -*-
import tushare as ts
import json
from bejond.basic import persistance


def get_last_date(code, collection_code):
    last_date = collection_code.find(
        {'code': code}
    ).sort([('date', -1)]).limit(1)

    if last_date.count() > 0:
        print last_date[0]['date']
        return last_date[0]['date']

    return None


# get_last_date('000868', collection_code = persistance.database.get_collection('stock_hist'))
