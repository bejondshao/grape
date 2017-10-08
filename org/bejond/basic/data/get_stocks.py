# !/usr/bin/python
# -*- coding: UTF-8 -*-


from bejond.basic import persistence
from bejond.basic import const


def get_stock_hist(code):
    collection_code = persistence.database.get_collection(const.STOCK_HIST)
    stock_hist = collection_code.find(
        {'code': code}
    ).sort([('date', 1)])