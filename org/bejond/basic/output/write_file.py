#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
from pathlib import Path

from bejond.basic.conn import hexo_path
from bejond.basic.const import HEXO_POST_HEAD, HEXO_POST_TITLE
from bejond.basic.util import dateu
from bejond.basic.util.static_string import FILE_MD


def write_head_up_to_post():
    """
    自动根据日期创建文件夹，博客文件，追加筛选内容
    以年为单位创建博客，方便复盘
    :return:
    """
    year = dateu.get_year()
    title = HEXO_POST_TITLE.format(a=year)
    home = str(Path.home()) # 用户目录
    path = home + hexo_path
    path_title = path + title

    if not os.path.isdir(path_title):
        print("Creating folder: " + path_title)
        os.mkdir(path_title)

        with open(path_title + FILE_MD, 'a') as file:
            print("Creating file: " + file.name)
            head = HEXO_POST_HEAD.format(a=year, b=dateu.get_now_time())
            file.write(head)

    with open(path_title + FILE_MD, 'a') as file:
        print("Appending file: " + file.name)
        file.write(str(year))
