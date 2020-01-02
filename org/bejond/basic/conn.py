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
# stock_basics表
collection_stock_basics = database.get_collection(stock_basics)
# stock_hist表
collection_stock_hist = database.get_collection(stock_hist)

# hexo post路径
hexo_path = config.get('hexo', 'hexo_hexo_post_path')