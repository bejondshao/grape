#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pandas
import tushare


df = tushare.get_hist_data('000800', start='2017-01-01')
#df = df.reset_index() # 将date(string)移到列中
df = df.sort_index(ascending=True)
#print(df)
ma_list = [30, 60]
for ma in ma_list:
    #df['ma_' + str(ma)] = pd.rolling_mean(df['close'], ma)
    df['ma_' + str(ma)] = pandas.Series(df['close']).rolling(window=ma).mean()

print(df)
