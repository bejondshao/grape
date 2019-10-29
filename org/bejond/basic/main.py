#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bejond.basic import index
from bejond.basic.analysis import mas_analysis
from bejond.basic.conn import database
from bejond.basic.data import fetch_stocks

# TODO 增加多个指标，根据不同自权重计算总权重，排序，而非像现在的通过或不通过
# TODO 开发修复某日数据的功能

def main():
    fetch_stocks.save_stock_hist()
    index.create_indexes()
    if len(database.collection_names()) > 0:
        fetch_stocks.repair_mas()

    mas_analysis.find_head_up(filter_time=1.3)

if __name__ == '__main__':
    main()
