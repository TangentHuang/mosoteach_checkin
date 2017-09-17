# -*- coding: utf-8 -*-
from datetime import datetime


def timer(week, rouge):
    """

    :param week: int 1-7
    :param rouge: (seconds, seconds)
    :return:
    """
    now = datetime.today()
    start, end = rouge
    if now.weekday() + 1 == week:
        if start <= now.hour * 60 + now.minute <= end:
            return True

    return False

# from time import sleep
# while True:
#     sleep(1)
#     print(timer(7, (21*60+30, 21*60+35)))