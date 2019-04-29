#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tushare as ts


def test_get_stock_basics():
    codes = ts.get_stock_basics()
    print(codes)


test_get_stock_basics()