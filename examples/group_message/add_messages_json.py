# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
import json

sys.path.insert(0, "../../")

from sdk.api.group_message import GroupMessage
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to add messages into group through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # Options(group_id, to, from, text) are mandatory. must be filled
    group_id = "GID57A82D462CBBF" # Group ID

    json_data = list()
    params = dict()
    params["to"] = "01000000000"
    params["from"] = "01000000000"
    params["text"] = "Test Message"

    # Optional parameters for your own needs
    # params["type"] = "SMS" # Message type ( SMS, LMS, MMS, ATA )
    # params["image_id"] = "image_id" # image_id. type must be set as 'MMS'
    # params["refname"] = "" # Reference name
    # params["country"] = "82" # Korea(82) Japan(81) America(1) China(86) Default is Korea
    # params["datetime"] = "20140106153000" # Format must be(YYYYMMDDHHMISS) 2014 01 06 15 30 00 (2014 Jan 06th 3pm 30 00)
    # params["subject"] = "Message Title" # set msg title for LMS and MMS
    # params["delay"] = "10") # '0~20' delay messages
    # params["sender_key"] = "5554025sa8e61072frrrd5d4cc2rrrr65e15bb64" # 알림톡 사용을 위해 필요합니다. 신청방법 : http://www.coolsms.co.kr/AboutAlimTalk
    # params["template_code"] = "C004" # 알림톡 template code 입니다. 자세한 설명은 http://www.coolsms.co.kr/AboutAlimTalk을 참조해주세요.

    json_data.append(params) # 원하는 만큼 params를 넣어줍니다
    json_data = json.dumps(json_data)

    cool = GroupMessage(api_key, api_secret)

    try:
        response = cool.add_messages_json(group_id, json_data)
        for data in response:
            print("Success Count : %s" % data['success_count'])
            print("Error Count : %s" % data['error_count'])

            if response['error_list']:
                print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
