#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bejond.basic.datamodel.stock_url import StockUrl

str1 = '000001'
int1 = int(str1)
print(int1)
print(str(int1))

stock_url = StockUrl('000010')
print(stock_url)