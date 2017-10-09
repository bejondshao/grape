# !/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import deque


class DataTotal:

    def __init__(self, cursor):
        """

        :param cursor: 从数据库获取的Cursor类型，其中包含close属性
        """
        days = cursor.count()
        self.data = deque(maxlen=days)
        self.total = 0.0
        for i in range(0, days):
            self.data.append(cursor[i]['close'])
            self.total += cursor[i]['close']

    def append(self, close):
        self.total = self.total - self.data.popleft() + close
        self.data.append(close)
