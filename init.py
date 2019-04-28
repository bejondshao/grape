#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import configparser


#  __location__ = os.path.realpath(
#    os.path.join(os.getcwd(), os.path.dirname(__file__)))

config = configparser.ConfigParser().read('config.ini')