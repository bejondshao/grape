# !/usr/bin/python
# -*- coding: UTF-8 -*-


from bejond.basic import conn
from bejond.basic import const


def get_stock_hist(code):
    stock_hist = conn.collection_stock_hist.find(
        {'code': code}
    ).sort([('date', 1)])