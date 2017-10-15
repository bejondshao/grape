# !/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import deque

import tushare
import json
from bejond.basic import const, conn
from bejond.basic.data import ma
from bejond.basic.util.dateu import date_delta


def get_last_date(code, collection_code):
    last_date = collection_code.find(
        {'code': code}
    ).sort([('date', -1)]).limit(1)

    if last_date.count() > 0:
        print(last_date[0]['date'])
        return last_date[0]['date']

    return None


# get_last_date('000868', collection_code = persistence.database.get_collection('stock_hist'))
val = deque(maxlen=3)
val.append('a')
print(len(val))
val.append('b')
val.append('c')
print(val)
print(len(val))
val.append('d')
print(val)
left = val.popleft()
print(left)
print(val)
right = val.append('e')
print(right)
print(val)

a = 1.0
a = a + 6 - 3
print(a)

df = tushare.get_k_data(code='000800', start='2017-10-01', end='2017-11-11')
print(df)

cursor = conn.collection_stock_basics.find_one()
for key in cursor:
    print(key)


# ma.repair_mas(conn.collection_stock_hist, '000800', const.DAYS_ARRAY)

print(date_delta('2017-01-02', '2017-01-04'))