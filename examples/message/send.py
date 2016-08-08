# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    ## 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'sms'
    params['to'] = '01000000000'
    params['from'] = '01000000000'
    params['text'] = 'Test Message'

    # Optional parameters for your own needs. more informations visit to http://www.coolsms.co.kr/SMS_API_v2#POSTsend
    # params["image"] = "desert.jpg" # image for MMS. type must be set as "MMS"
    # params["image_encoding"] = "binary" # image encoding binary(default), base64 
    # params["mode"] = "test" # 'test' 모드. 실제로 발송되지 않으며 전송내역에 60 오류코드로 뜹니다. 차감된 캐쉬는 다음날 새벽에 충전 됩니다.
    # params["delay"] = "10" # 0~20사이의 값으로 전송지연 시간을 줄 수 있습니다.
    # params["force_sms"] = "true" # 푸시 및 알림톡 이용시에도 강제로 SMS로 발송되도록 할 수 있습니다.
    # params["refname"] = "" # Reference name
    # params["country"] = "KR" # Korea(KR) Japan(JP) America(USA) China(CN) Default is Korea
    # params["sender_key"] = "5554025sa8e61072frrrd5d4cc2rrrr65e15bb64" # 알림톡 사용을 위해 필요합니다. 신청방법 : http://www.coolsms.co.kr/AboutAlimTalk
    # params["template_code"] = "C004" # 알림톡 template code 입니다. 자세한 설명은 http://www.coolsms.co.kr/AboutAlimTalk을 참조해주세요. 
    # params["datetime"] = "20140106153000" # Format must be(YYYYMMDDHHMISS) 2014 01 06 15 30 00 (2014 Jan 06th 3pm 30 00)
    # params["mid"] = "mymsgid01" # set message id. Server creates automatically if empty
    # params["gid"] = "mymsg_group_id01" # set group id. Server creates automatically if empty
    # params["subject"] = "Message Title" # set msg title for LMS and MMS
    # params["charset"] = "euckr" # For Korean language, set euckr or utf-8
    # params["app_version] = "Python SDK v2.0" # 어플리케이션 버전

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
