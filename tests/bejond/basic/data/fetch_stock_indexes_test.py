#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bejond.basic import const
from org.bejond.basic.data import fetch_stock_indexes
from org.bejond.basic import conn

#conn.database.drop_collection('stock_indexes')

fetch_stock_indexes.save_stock_index_hist(start_date='2010-01-01')

stock_indexes = conn.collection_stock_indexes

total = {}
for index in const.STOCK_INDEXES:
    total[index] = {1: {'positive': 0, 'negative': 0}, 2: {'positive': 0, 'negative': 0}, 3: {'positive': 0, 'negative': 0}, 4: {'positive': 0, 'negative': 0}, 5: {'positive': 0, 'negative': 0}}
for stock_index in stock_indexes.find():
    code = stock_index['code']
    day_of_week = stock_index['day_of_week']
    if stock_index['p_change'] > 0:
        total[code][day_of_week]['positive']+=1
    elif stock_index['p_change'] < 0:
        total[code][day_of_week]['negative']+=1
    if 'total_p' not in total[code][day_of_week]:
        total[code][day_of_week]['total_p'] = 0
        total[code]['name'] = stock_index['name']
    if 'total_price' not in total[code][day_of_week]:
        total[code][day_of_week]['total_price'] = 0
    total[code][day_of_week]['total_p'] += stock_index['p_change']
    total[code][day_of_week]['total_price'] += stock_index['price_change']

for index in const.STOCK_INDEXES:
    for i in range(5): # in range doesn't count range
        i+=1
        current_code_day = total[index][i]
        total_days = current_code_day['positive'] + current_code_day['negative']
        if total_days > 0:
            current_code_day['negative_rate'] = round(current_code_day['negative'] / (total_days), 2)

print(total)

