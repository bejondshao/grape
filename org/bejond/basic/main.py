#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bejond.basic import index, conn
from bejond.basic.analysis import mas_analysis
from bejond.basic.conn import database
from bejond.basic.data import fetch_stocks

# TODO 增加多个指标，根据不同自权重计算总权重，排序，而非像现在的通过或不通过
# TODO 开发修复某日数据的功能
from bejond.basic.util import dateu
from bejond.basic.util.dateu import calculate_delta


def main():
    fetch_stocks.save_stock_hist()
    index.create_indexes(conn.collection_stock_hist, index.stock_hist_index_array)
    if len(database.list_collection_names()) > 0:
        fetch_stocks.repair_mas()

    mas_analysis.find_head_up(filter_time=1.3)
    index.create_indexes(conn.collection_stock_ma_head_up, index.stock_ma_head_up_index_array)

if __name__ == '__main__':
    date1 = dateu.now()
    main()
    date2 = dateu.now()
    calculate_delta(date1, date2)
