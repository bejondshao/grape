#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json

import tushare


def fetch_industry():
    """

    :return:
    """
    df = tushare.get_industry_classified()
    print(df)
