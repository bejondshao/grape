# !/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import requests

from bejond.basic.const import GTIMG_URL


def fetch_index(code, date='2010-01-01', url=GTIMG_URL):
    url = url.format(code=code, date=date)
    response_obj = requests.get(url).json()  # returns a python object, dictionary
    # response = requests.get(url).text
    print(response_obj)
    # response_json = json.dumps(response_obj)  # this is raw json
    # print(response_json)
    return response_obj
