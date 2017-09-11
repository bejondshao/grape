# !/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
import urllib2
import json
import persistance
from bson import json_util

url = 'http://www.ctxalgo.com/api/stocks'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
stock_basics = persistance.database['stock_basics2']
read = response.read()
dict = json_util.loads(read)
items = dict.items()
stock_basics.insert_many(dict)
