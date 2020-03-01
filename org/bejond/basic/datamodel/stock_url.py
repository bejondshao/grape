#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bejond.basic import conn
from bejond.basic.util.static_string import SH, SZ, SIX, O


class StockUrl(object):

    def __init__(self, code):
        self.code = code
        self.no_zero_code = code
        self.market = SH
        self.market_stock_code = self.market + code
        self.lixinger_url = conn.lixinger_url
        self.xueqiu_url = conn.xueqiu_url
        self.eastmoney_url = conn.eastmoney_url
        self.__refresh()

    def __deal_market(self):
        """
        根据代码返回所属市场
        :param code:
        :return:
        """
        if not self.code.startswith(SIX):
            self.market = SZ
            self.market_stock_code = self.market + self.code
            if self.code.startswith(O):
                no_zero_int = int(self.code)
                self.no_zero_code = str(no_zero_int)

    def __deal_lixinger_url(self):
        """
        根据代码转换理性人的url
        :param code:
        :return:
        """
        self.lixinger_url = self.lixinger_url.format(market=self.market, code=self.code, no_zero_code=self.no_zero_code)

    def __deal_xueqiu_url(self):
        """
        根据代码转换雪球的url
        :return:
        """
        self.xueqiu_url = self.xueqiu_url.format(market_stock_code=self.market_stock_code)

    def __deal_eastmoney_url(self):
        """
        根据代码转换东方财富的url
        :return:
        """
        self.eastmoney_url = self.eastmoney_url.format(code=self.code)

    def __refresh(self):
        """
        将SotckUrl中的属性都处理并重新设置
        :return:
        """
        self.__deal_market()
        self.__deal_lixinger_url()
        self.__deal_xueqiu_url()
        self.__deal_eastmoney_url()

    def __repr__(self):
        return str(self.__dict__)
