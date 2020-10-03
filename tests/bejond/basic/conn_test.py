#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from org.bejond.basic import conn
from org.bejond.basic.data import fetch_stocks

conn1 = conn.collection_indexes
print(conn1)  # Collection(Database(MongoClient(host=, document_class=dict, ), ), 'indexes')
last_date = fetch_stocks.get_last_date('sh0000001', conn.collection_indexes)
print(last_date)  # 如果conn1的表不存在，last_date是None，不会报错
