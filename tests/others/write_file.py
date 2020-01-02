#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import subprocess

# 打开文件，并追加，将执行命令的内容写入test.txt中
from bejond.basic.const import HEXO_POST_HEAD
from bejond.basic.output.write_file import write_head_up_to_post

with open('test.txt', 'a') as file:
    str = HEXO_POST_HEAD.format(a='2020', b='2020-01-02')
    file.write(str)
    # 经验：需要是指定string调用format，不可用连接"+"，只会对"+"后面的string格式化


# 测试创建文件夹和文件，写入指定的头信息，后续追加内容。
# 测试通过
write_head_up_to_post()