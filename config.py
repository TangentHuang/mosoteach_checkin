# -*- coding: utf-8 -*-


class SimpleConfig:
    # 登陆请求的返回JSON中可以找到
    USER_ID = None
    ACCESS_SECRET = None

    # 签到请求的headers中可以找到
    X_MSSVC_ACCESS_ID = None
    X_MSSVC_SEC_TS = None

    # 每次请求的延迟时间范围, 秒
    INTERVAL = (10, 20)

    # 日志的位置
    LOGGING_PATH = "./logging.txt"

    # 经纬度
    # LNG = "100.000000"
    # LAT = "100.000000"
    LNG = None
    LAT = None

    CLAZZ_COURSE_ID = None




configs = {
    'simple': SimpleConfig,
}

