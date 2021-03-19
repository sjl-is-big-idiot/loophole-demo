# _*_ coding: utf-8 _*_
# @FileName : tools.py
# @Author   : sjl
# @CreatedAt     :  2021/03/19 11:04:44
# @UpdatedAt     :  2021/03/19 11:04:44
# @description: tool functions
# @Software : VSCode


from logger import SimpleLogger
import time
from functools import wraps


sp_logger = SimpleLogger(__name__, "./log/loophole.log").get_logger()


def spend_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        sp_logger.info("executing {} spend time = {} s".format(func, time.time()-start_time))

    return wrapper
