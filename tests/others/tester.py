#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from collections import deque

import tushare

from bejond.basic import conn
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
tushare.set_token('613539b4845cb7f8d0c5ef32bde871095130009e2244da8190257326')
pro = tushare.pro_api()

df_pro = pro.daily(ts_code='600466.SH', start_date='20181019') # tuahre pro
print(df_pro)
df_pro_bar = tushare.pro_bar(ts_code='600466.SH', adj='qfq', start_date='20181019')
print(df_pro_bar)

df = tushare.get_k_data(code='600466', start='2018-10-19')
print(df)

cursor = conn.collection_stock_basics.find_one()
print(cursor['name'])
for key in cursor:
    print(key)

# ma.repair_mas(conn.collection_stock_hist, '000800', const.DAYS_ARRAY)

print(date_delta('2017-01-02', '2017-01-04'))

print(60 / 8)
print(int(60 / 8))
print(2.9 / 7)