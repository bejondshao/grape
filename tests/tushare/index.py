#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tushare as ts


df = ts.get_sina_dd('601699', date='2020-07-03', vol=10000)
print(df)