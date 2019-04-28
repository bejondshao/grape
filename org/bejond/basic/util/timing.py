# !/usr/bin/python
# -*- coding: UTF-8 -*-

# python3
import atexit
from time import time
from datetime import timedelta
# python3
import atexit
from datetime import timedelta
from time import time


def seconds_to_str(t):
    return str(timedelta(seconds=t))


line = "=" * 40


def log(s, elapsed=None):
    print(line)
    print(seconds_to_str(time()), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)


def end_log():
    end = time()
    elapsed = end - start
    log("End Program", seconds_to_str(elapsed))


def now():
    return seconds_to_str(time())


start = time()
atexit.register(end_log)
log("Start Program")
