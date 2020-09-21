#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pandas

from bejond.basic import conn
from bejond.basic.conn import collection_stock_ma_head_up
from bejond.basic.data import ma
from bejond.basic.datamodel.code_ma_head_up import CodeMaHeadUp
from bejond.basic.datamodel.one_day import OneDay
from bejond.basic.output.write_file import write_head_up_to_post
from bejond.basic.util import dateu


def find_head_up(code=None, start=None, end=None, pb=4, pe=40, delta=60, filter_time=1.5, write_and_store=True):
    """
    根据ma_60计算趋势，可以将计算结果代码，组合成url直接在某个网站打开。
    :param code:
    :param start:
    :param end:
    :param pb:
    :param pe:
    :param delta:
    :param filter_time:
    :param write_and_store: 将结果存入数据库并写入博客中。测试时设为False
    :return:
    """
    print('\n')
    if end is None:
        end = dateu.get_today_str()
    print(end)
    print("find_head_up(filter_time=" + str(filter_time) + ")")
    # previous = dateu.get_previous_date_str(100) # 查找100天前上市的
    time_limit = dateu.get_today_int() - 10000 # 查找一年前上市的股票
    codes = conn.collection_stock_basics.find(
        {'timeToMarket': {'$lt': time_limit}, 'pb': {'$lt': pb}, 'pe': {'$lt': pe, '$gt': 0}}, # 总资产小于500亿
        {'code': 1, 'name': 1, 'industry': 1, 'area': 1, 'pb': 1, 'pe': 1, '_id': 0})  # codes为Cursor {'code': 'xxxxxx', 'name": 'xxxx', 'industry': 'xxxx', 'area': 'xx'}

    code_date_list = []
    # 用于检查delta日期之内的股票
    delta_date = dateu.get_previous_date_str(delta)
    today = dateu.get_today_str()
    for code_cursor in codes:  # 分析每只股票
        code = code_cursor['code']
        # code = '600741'
        histories = pandas.DataFrame(list(conn.collection_stock_hist.find(
            {'code': code, 'ma_60': {'$gt': 0}}).sort([('date', -1)]).limit(delta)))
        histories = histories[::-1]  # reverse所查询的结果，将早的日期放到前面
        first = None
        second = None

        days_list = []
        for history in histories.itertuples():  # 根据股票历史计算没两天股票斜率，并放到list中
            date = getattr(history, 'date')
            close = getattr(history, 'close')
            ma_60 = getattr(history, 'ma_60')
            if first is None:
                first = OneDay(code, date, close, ma_60)
                continue

            second = OneDay(code, date, close, ma_60)
            second.slope = second.get_slope(first)
            days_list.append(second)
            first = second

        # for history in histories:  # 根据股票的历史，组合成前后两天为一组的数据模型
        #     date = history['date']
        #     close = history['close']
        #     ma_60 = history['ma_60']
        #     if first is None:
        #         first = OneDay(date, close, ma_60)
        #         continue
        #
        #     second = OneDay(date, close, ma_60)
        #     two_days = TwoDays(first, second)
        #     two_days_list.append(two_days)
        #     first = second

        if len(days_list) > 0:  # 根据斜率变化，判断股票走势
            if start is None:
                start = dateu.get_previous_date_str(int(delta / 8)) # 这里int(delta / 8)只是计算观察区间，8是随意取的值，int(60 / 8) = 7，也就是前7天
            day_first = None
            for day in days_list:
                if day_first is None:
                    day_first = day
                    continue
                if day_first.slope < 0 <= day.slope and start < day.date <= end and day.close > day.ma_60: # day.close >= day.ma_60是必要的，可以过滤掉中途凸起又下落的股票
                    max = ma.get_recent_max(code) # 对符合ma的值向前一年内所处位置进行筛选，最高点要低于当前值的1.5倍，最低点的1.5倍要高于当前值
                    min = ma.get_recent_min(code)
                    if max / filter_time <= day.close <= min * filter_time:
                        print(code + ' ' + code_cursor['name'] + ' ' + code_cursor['industry'] + ' ' + code_cursor['area'] + ': ' + day.date + ' 收盘价: ' + str(day.close))
                        fetched_stock = collection_stock_ma_head_up.find_one({'code':code, 'date': {'$gt' : delta_date}}) # delta_date在这里是str，所以后面的日期比前面的日期大
                        if fetched_stock is None:
                            stock_filtered = CodeMaHeadUp(code, name=code_cursor['name'], date=day.date, industry=code_cursor['industry'], area=code_cursor['area'], close=str(day.close), today=today)
                            print("=================================================================================")
                            print("inserting: {0}, {1}, {2}".format(stock_filtered.code, stock_filtered.name, stock_filtered.date))
                            print("=================================================================================")
                            if write_and_store:
                                collection_stock_ma_head_up.insert_one(stock_filtered.__dict__)
                                if code_cursor['pb'] < 4 and code_cursor['pe'] < 40:
                                    code_date_list.append(stock_filtered)
                            break
                # elif day_first.slope > 0:
                #     break
                else:
                    day_first = day

    print(len(code_date_list))
    if write_and_store:
        write_head_up_to_post(code_date_list)
    print('----------------------------------------------------------------------------')

    return code_date_list


"""
    执行完fetch_stocks.py的save_stock_hist()和repair_mas()后，执行find_head_up()，查找开启抬头的股票。
    有个小问题，就是有时候会选出涨到顶峰的股票。
"""
