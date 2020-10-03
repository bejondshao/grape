#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json

from bejond.basic import const, conn
from bejond.basic.data import fetch_stocks
from bejond.basic.util import dateu
from bejond.basic.util import rest_util


def save_stock_index_hist(start_date=None, checks=None):
    """
    更新指数历史，建议每日收盘后运行。因为收盘前运行当日数据会有误
    :param start_date: 获取指数的起始日期。
    :param checks: 临时更新某些指数的历史，节省时间。checks=None时更新所有指数历史。
    :return:
    """
    codes = const.STOCK_INDEXES
    i = 1
    if checks is not None:
        codes = checks

    # calculate end out of for loop to save time. end is date
    end = None
    if fetch_stocks.is_before_close_time():
        end = dateu.get_previous_date()
    # 这里需要传end，如果是在交易日日中执行获取数据，则获取日期截止到前一个交易日，作为最新的交易日
    latest_trade_date_str = dateu.get_latest_trade_date_str(end)
    # 存储当日获取指数指数
    code_list = []
    for code in codes:
        last_date = None
        # persistence.database.drop_collection(code)
        # if collection_code is not None:
        # last_result = collection_code.find({}).sort('date', -1).limit(1)
        #    last_result = collection_code.find({}).sort({'date': -1}).limit(1)

        # df_hist_data = None
        # 上一次获取数据的最后交易日期
        last_date = fetch_stocks.get_last_date(code, conn.collection_stock_indexes)

        if last_date is None:  # 如果数据库未找到上一次存储的日期，说明是新指数
            hist_data = rest_util.fetch_index(code, start_date)
            code_list.append(code)
        elif last_date.__eq__(latest_trade_date_str):  # 如果last_date和最新交易日（如果今天此时时间不到收盘时间，则是上一个交易日。如果时间是收盘时间后，则是今天）一样，说明获取过，就跳过
            # elif last_date.__eq__(dateu.get_previous_date_str(1)): # 这一行是周六测试用，忽略
            continue
        else:  # 如果找到上次存储的日期且日期不是最近的交易日
            # next_trade_date = dateu.get_next_trade_date(last_date) # 获取下个交易日，is_holiday读取csv速度太慢，放弃
            # if next_trade_date < datetime.now():
            print(str(i) + '. ' + code)
            code_list.append(code)
            print('last_date ' + str(last_date))
            repeat = True
            while repeat:
                try:
                    hist_data = rest_util.fetch_index(code, last_date)
                    repeat = False
                except Exception as e:
                    continue

        # hist_data contains 'code', api status code, 'msg', apt message, 'data', index data. 'data' contains real_code attribute, like 'sh000001'.
        # 'sh000001' is hist_obj
        if hist_data is not None:
            # hist_obj contains 'day', 'qt', 'mx_price', 'prec', 'version'. 'day' is an array, in each element, is also an array.
            # 'qt' contains 'sh000001', 'market', 'zhishu'. 'sh000001' is array
            hist_obj = hist_data['data'][code]
            hist_qt = hist_obj['qt'][code]
            if 'day' not in hist_obj:
                hist_day_arr = hist_obj['qfqday']
            else:
                hist_day_arr = hist_obj['day']
            index_list = list()
            name = hist_qt[1] # .encode('utf-8').decode('unicode_escape') # unicode转为中文
            last_day = None
            for day in hist_day_arr:
                date = day[0]
                day_of_week = dateu.day_of_week_str(date)
                daily = {'code': code, 'name': name, 'date': date, 'open': float(day[1]), 'close': float(day[2]),
                         'high': float(day[3]), 'low': float(day[4]), 'volume': float(day[5]), 'day_of_week': day_of_week}
                if last_day is None:
                    daily['price_change'] = 0
                    daily['p_change'] = 0.00
                else:
                    daily['price_change'] = daily['close'] - last_day['close']
                    daily['p_change'] = round(daily['price_change'] * 100 / last_day['close'], 3)
                last_day = daily
                index_list.append(daily)
            # 自行计算ma_30和ma_60
            # hist_arr = mas(conn.collection_indexes, code, const.INDEX_DAYS_ARRAY, hist_obj)

            conn.collection_stock_indexes.insert_many(index_list) # json.loads(index_arr.to_json(orient='records'))
        i += 1

    return code_list
