# -*- coding: UTF-8 -*-

from pymongo import MongoClient

import configparser
import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
# 配置文件
config = configparser.ConfigParser()
config.read(__location__ + '/../../../config.ini')
# 数据库客户端
client = MongoClient(config.get('database', 'host'), int(config.get('database', 'port')))
# 数据库
database = client[config.get('database', 'database_name')]
# 表名
stock_basics = config.get('collection', 'stock_basics')
# 表名
stock_hist = config.get('collection', 'stock_hist')
# stock_basics表
collection_stock_basics = database.get_collection(stock_basics)
# stock_hist表
collection_stock_hist = database.get_collection(stock_hist)
