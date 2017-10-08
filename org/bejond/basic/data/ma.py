# !/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division

from collections import deque
from org.bejond.basic import persistence
from bejond.basic import const


def ma(days):
    collection_code = persistence.database.get_collection(const.STOCK_HIST)
    codes = list(persistence.database.get_collection(const.STOCK_BASICS).find({},{'code': 1, '_id': 0}))
    for code in codes:
        print(code['code'])

    for code in codes:
        code = {'code':'000800'}
        stock_hist = collection_code.find({'code': code['code']}).sort([('date', 1)])
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


ma(days=60)
