import datetime
import time
import bejond.basic.util.dateu as dateu

localtime = time.localtime(time.time())
now = dateu.now()
today_str = dateu.get_today_str()
today = dateu.get_today()
today3pm = dateu.get_close_time()
print('localtime:', localtime)
print('today_str:', today_str)
print('now:', now)
print('today:', today)
print('today3pm:', today3pm)
print('now is previous than 3pm:', now < today3pm)

# ===============================
'''
localtime: time.struct_time(tm_year=2019, tm_mon=5, tm_mday=19, tm_hour=18, tm_min=7, tm_sec=6, tm_wday=6, tm_yday=139, tm_isdst=0)
today_str: 2019-05-19
now: 2019-05-19 18:07:06.262168
today: 2019-05-19 00:00:00
today3pm: 2019-05-19 15:00:00
now is previous than 3pm: False
'''
