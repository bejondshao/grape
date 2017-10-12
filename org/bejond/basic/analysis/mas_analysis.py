# !/usr/bin/python
# -*- coding: UTF-8 -*-

from bejond.basic import conn, const


def find_head_up():
    codes = conn.collection_stock_basics.find({}, {'code': 1, '_id': 0})