# !/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum

class OneDay:
    def __init__(self, code, date, close, ma_60):
        self.code = code
        self.date = date
        self.close = close
        self.ma_60 = ma_60
        self.slope = None

    def get_slope(self, first):
        return self.ma_60 - first.ma_60

    def downing(self, first):
        """

        :param first:
        :return: 1代表斜率倾斜度变小，0代表斜率倾斜度变大，-1代表斜率为正数
        """
        if first.slope < 0:
            minus = self.slope - first.slope
            if minus >= 0:
                return Slope.DOWN_SLOW
            else:
                return Slope.DOWN_FAST
        else:
            return Slope.UP

    #def get_next_bigger_slope_day(self, days_list):
        # if self.downing(days_list[0]):


class Slope(Enum):
    DOWN_FAST = -1
    DOWN_SLOW = 0
    UP = 1
