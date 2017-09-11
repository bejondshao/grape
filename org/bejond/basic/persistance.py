# !/usr/bin/python
# -*- coding: UTF-8 -*-

from pymongo import MongoClient
import configparser
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = configparser.ConfigParser()
config.read(__location__ + '/../../../config.ini')
client = MongoClient(config.get('database', 'host'), int(config.get('database', 'port')))
database = client[config.get('database', 'databaseName')]
