#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tushare as ts


def test_get_stock_basics():
    codes = ts.get_stock_basics()
    print(codes)


#test_get_stock_basics()

#ts.get_hist_data('128023')
df = ts.new_cbonds()
df = df[['bcode', 'bname', 'scode', 'sname', 'xcode', 'convprice', 'ipo_date', 'issue_date']]
print(df.head(10))
#ts.bar('128023')