# !/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import deque

import tushare
import json
from bejond.basic import persistence


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