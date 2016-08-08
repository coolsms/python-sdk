# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to check cash & point balance through CoolSMS Rest API PHP
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    cool = Message(api_key, api_secret)
    try:
        response = cool.balance()
        print("Cash : %s" % response['cash']) # 남은 캐쉬
        print("Point : %s" % response['point']) # 남은 포인트
        print("Deferred Payment: %s" % response['deferred_payment']) # 후불회원인지 확인
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
