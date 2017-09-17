# -*- coding: utf-8 -*-
import requests
import sys
import json
import logging
from time import sleep
from random import randint
from datetime import datetime, timedelta

from config import configs
from tools import get_checkin_signature, get_current_open_signature
from tools import timer



class ResultCodeError(Exception):
    """http请求返回了未知的码"""
    pass


class Checkin:

    def __init__(self, config):
        self._config = configs[config]

        self._logger = logging.Logger(__name__)
        console_hander = logging.StreamHandler()
        console_hander.setFormatter(logging.Formatter("%(asctime)s %(levelname)s:%(message)s"))
        console_hander.setLevel(logging.DEBUG)
        console_hander.addFilter(logging.Filter(__name__))
        self._logger.addHandler(console_hander)

        file_hander = logging.FileHandler(filename=self._config.LOGGING_PATH, mode='a', encoding='utf-8')
        file_hander.setFormatter(logging.Formatter("%(asctime)s %(levelname)s:%(message)s"))
        file_hander.setLevel(logging.INFO)
        self._logger.addHandler(file_hander)

    def checkin(self, checkin_id):
        self._logger.info('开始签到')
        today = datetime.today() - timedelta(seconds=60 * 60 * 8 + 10)
        date = today.strftime("%a, %d %b %Y %H:%M:%S GMT+00:00")

        url = "http://checkin.mosoteach.cn:19527/checkin"

        headers = {
            "Accept-Encoding": "gzip;q=0.7,*;q=0.7",
            "User-Agent": "Dalvik/2.1.0 Linux; U; Android 7.1.1;",
            "Date": date,
            "X-device-code": "oefxef1d_3df_dkfl2_dkfj_df_dkfjkdfda",
            "X-mssvc-signature": get_checkin_signature(date, self._config),
            "X-mssvc-access-id": self._config.X_MSSVC_ACCESS_ID,
            "X-app-id": "MTANDROID",
            "X-app-version": "2.4.0",
            "X-mssvc-sec-ts": self._config.X_MSSVC_SEC_TS,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Content-Length": "64",
            "Host": "checkin.mosoteach.cn:19527",
        }

        data = {
            "checkin_id": checkin_id,
            "report_pos_flag": "Y",
            "lat": self._config.LAT,
            "lng": self._config.LNG,
        }

        r = requests.post(url, headers=headers, data=data)
        resp = json.loads(r.text)
        if resp['result_code'] == 2409:
            self._logger.info("重复签到, 返回的值: {}".format(r.text))
            return False
        if resp['result_code'] == 0:
            self._logger.info("签到完毕, 返回的值: {}".format(r.text))
            return True
        self._logger.info("签到失败, 返回的值: {}".format(r.text))
        return False



    def get_checkin_id(self):
        today = datetime.today() - timedelta(seconds=60 * 60 * 8 + 10)
        date = today.strftime("%a, %d %b %Y %H:%M:%S GMT+00:00")


        headers = {
            "Accept-Encoding": "gzip;q=0.7,*;q=0.7",
            "User-Agent": "Dalvik/2.1.0 Linux; U; Android 7.1.1;",
            "Date": date,
            "X-device-code": "oefxef1d_3df_dkfl2_dkfj_df_dkfjkdfda",
            "X-mssvc-signature": get_current_open_signature(date, self._config),
            "X-mssvc-access-id": self._config.X_MSSVC_ACCESS_ID,
            "X-app-id": "MTANDROID",
            "X-app-version": "2.4.0",
            "X-mssvc-sec-ts": self._config.X_MSSVC_SEC_TS,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Content-Length": "52",
            "Host": "api.mosoteach.cn",
        }

        data = {
            "clazz_course_id": self._config.CLAZZ_COURSE_ID,
        }

        r = requests.post("http://api.mosoteach.cn/mssvc/index.php/checkin/current_open", headers=headers, data=data)

        resp = json.loads(r.text)
        if resp["result_code"] == 1001:
            self._logger.info("未签到")
            return -1
        elif resp["result_code"] == 0:
            self._logger.info("准备签到， 签到码: {}".format(resp['id']))
            return resp["id"]
        else:
            raise ResultCodeError("未知错误返回码: {}".format(resp))

    def monitor(self):
        self._logger.info("开始监听签到")
        while True:
            sleep(randint(*self._config.INTERVAL))
            if timer(1, (8*60+8, 9*60+50)):
                checkin_id = self.get_checkin_id()
                if checkin_id != -1:
                    self.checkin(checkin_id)
                    return
            else:
                self._logger.debug("未在监听时段")



if __name__ == '__main__':
    Checkin(config=sys.argv[1]).monitor()


