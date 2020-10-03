# -*- coding: UTF-8 -*-

import configparser
import os

from pymongo import MongoClient

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
# 表名
stock_indexes = config.get('collection', 'stock_indexes')
# stock_ma_head_up表名
stock_ma_head_up = config.get('collection', 'stock_ma_head_up')
# stock_basics表
collection_stock_basics = database.get_collection(stock_basics)
# stock_hist表
collection_stock_hist = database.get_collection(stock_hist)
# indexes表
collection_stock_indexes = database.get_collection(stock_indexes)
# stock_ma_head_up表
collection_stock_ma_head_up = database.get_collection(stock_ma_head_up)

# hexo post路径
hexo_path = config.get('hexo', 'hexo_hexo_post_path')

# stock
lixinger_url = config.get('stock', 'lixinger_url')
xueqiu_url = config.get('stock', 'xueqiu_url')
eastmoney_url = config.get('stock', 'eastmoney_url')