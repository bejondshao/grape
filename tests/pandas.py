# !/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts


df = ts.get_hist_data('000800', start='2017-01-01')
ma_list = [5, 10, 20, 30, 60]
for ma in ma_list:
    df['ma_' + str(ma)] = pd.rolling_mean(df['close'], ma)

print df