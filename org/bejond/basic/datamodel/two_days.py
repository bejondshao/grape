# -*- coding: UTF-8 -*-


class TwoDays(object):
    def __init__(self, first, second):
        """

        :param cursor: 从数据库获取的Cursor类型，其中包含close属性
        """
        self.first = first
        self.second = second

    def get_k(self):
        return self.second.ma_60 - self.first.ma_60
