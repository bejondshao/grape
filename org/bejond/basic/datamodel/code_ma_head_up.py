# -*- coding: UTF-8 -*-
from bejond.basic.util.static_string import SPAN


class CodeMaHeadUp(object):
    def __init__(self, code, name, date, industry, area, close, today):
        self.code = code
        self.name = name
        self.date = date
        self.industry = industry
        self.area = area
        self.close = close
        self.insert_date = today

    def attributes(self):
        return ['code', 'name', 'date', 'industry', 'area', 'close']

    def __lt__(self, other):
        return self.date < other.date

    def to_md_table(self):
        """
        将对象转换为"|601211|国泰君安|2019-12-30|证券|上海|18.68|"形式，输出为markdown的table一行
        :return:
        """
        to_string = SPAN
        for attribute in self.attributes():
            to_string += self.__getattribute__(attribute) + SPAN
        return to_string

    """
        def __repr__(self):
            return str(self.__dict__)
    """
