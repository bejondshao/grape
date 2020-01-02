#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tushare as ts

pro = ts.pro_api('5683e168c0c9f0f7d9066cead21854067738e997dcd0e204275f8dd4')
data = pro.hsgt_top10(trade_date='20180725', market_type='1')
print(data)
df = pro.top_list(trade_date='20191119')
print(df)
df = pro.top_inst(trade_date='20191119')
print(df)