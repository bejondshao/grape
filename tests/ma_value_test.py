#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy
import pandas

percent = 0.1
base1 = 1
base2 = 479.0
list1 = []
list2 = []
first1 = base1 * (1 + percent)
first2 = base2 * (1 + percent)
for i in range(0, 20):
    list1.append(first1)
    list2.append(first2)
    first1 = first1 * (1 + percent)
    first2 = first2 * (1 + percent)

print(list1)
print(list2)
df1 = pandas.DataFrame(list1, columns=['close'])
df2 = pandas.DataFrame(list2, columns=['close'])
df1['ma_' + str(5)] = pandas.Series(df1['close']).rolling(window=5).mean()
df2['ma_' + str(5)] = pandas.Series(df2['close']).rolling(window=5).mean()
print(df1)
print(df2)
cal11 = df1.iloc[18]['ma_5'] - df1.iloc[17]['ma_5']
cal12 = df1.iloc[19]['ma_5'] - df1.iloc[18]['ma_5']
a = cal12 - cal11
k1_base = a / df1.iloc[17]['close']
print(k1_base)
cal21 = df2.iloc[18]['ma_5'] - df2.iloc[17]['ma_5']
cal22 = df2.iloc[19]['ma_5'] - df2.iloc[18]['ma_5']
b = cal22 - cal21
print(b)
print(numpy.isclose(a, b / base2))
k2_base = b / df2.iloc[17]['close']
print(k2_base)
print(k1_base == k2_base)
