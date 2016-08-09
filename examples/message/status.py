# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


##  @brief This sample code demonstrate how to check sms result through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # Optional parameters for your own needs
    params = dict()
    # params["count"] = "1" # 기본값 1이며 1개의 최신 레코드를 받을 수 있음. 10입력시 10분동안의 레코드 목록을 리턴
    # params["unit"] = "minute" # minute(default), hour, day 중 하나 해당 단위의 평균
    # params["date"] = "20161016230000" # 데이터를 읽어오는 기준 시각 
    # params["channel"] = "1" # 1 : 1건 발송채널(default), 2 : 대량 발송 채널

    cool = Message(api_key, api_secret)
    try:
        response = cool.status()
        for data in response:
            print("Registdate : %s" % data['registdate'])
            print("SMS average : %s" % data['sms_average'])
            print("SMS sk_average : %s" % data['sms_sk_average'])
            print("SMS kt_average : %s" % data['sms_kt_average'])
            print("SMS lg_average : %s" % data['sms_lg_average'])
            print("MMS average : %s" % data['mms_average'])
            print("MMS sk_average : %s" % data['mms_sk_average'])
            print("MMS kt_average : %s" % data['mms_kt_average'])
            print("MMS lg_average : %s" % data['mms_lg_average'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
