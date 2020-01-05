#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from time import sleep

from bejond.basic.util import dateu

print(dateu.get_latest_trade_date_str())

date1 = dateu.now()
sleep(2.2)
date2 = dateu.now()
dateu.calculate_delta(date1, date2)

print(dateu.get_previous_date())