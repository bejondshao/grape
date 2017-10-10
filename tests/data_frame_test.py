# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas

df1 = pandas.DataFrame({
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        },
                        )

df2 = pandas.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                         index=[4, 5, 6, 7])

frames = [df1, df2]

result = pandas.concat(frames)

print(result)