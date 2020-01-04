#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
from pathlib import Path

from bejond.basic.conn import hexo_path
from bejond.basic.const import HEXO_POST_HEAD, HEXO_POST_TITLE
from bejond.basic.datamodel.stock_url import StockUrl
from bejond.basic.util import dateu, md_util
from bejond.basic.util.md_util import to_url_open
from bejond.basic.util.static_string import FILE_MD


def write_head_up_to_post(list, new_table=False):
    """
    自动根据日期创建文件夹，博客文件，追加筛选内容
    以年为单位创建博客，方便复盘
    :param list 要输出的类的列表，这里为CodeMaHeadUp的集合
    :return:
    """
    if len(list) > 0:
        list.sort()
        year = dateu.get_year()
        title = HEXO_POST_TITLE.format(a=year)
        home = str(Path.home()) # 用户目录
        path = home + hexo_path
        path_title = path + title
        new_head = md_util.to_table_head(list[0])
        if not os.path.isdir(path_title):
            print("Creating folder: " + path_title)
            os.mkdir(path_title)

            with open(path_title + FILE_MD, 'a') as file:
                print("Creating file: " + file.name)
                head = HEXO_POST_HEAD.format(a=year, b=dateu.get_now_time())
                file.write(head)
                file.write(new_head)

        with open(path_title + FILE_MD, 'a') as file:
            print("Appending file: " + file.name)
            if new_table:
                print("Creating new table")
                file.write(new_head)
            for cls in list:
                stock = StockUrl(cls.code)
                to_url_open(stock, cls)
                row = md_util.to_table_row(cls)
                print(row)
                file.write(row)
