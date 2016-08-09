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
    params['type'] = 'ata' # Message type ( sms, lms, mms, ata )
    params['to'] = '01000000000' # Recipients Number '01000000000,01000000001'
    params['from'] = '01000000000' # Sender number
    params["sender_key"] = "#ENTER_YOUR_SENDER_KEY#" # 알림톡 사용을 위해 필요합니다. 신청방법 : http://www.coolsms.co.kr/AboutAlimTalk
    params["template_code"] = "#ENTER_YOUR_TEMPLATE_CODE#" # 알림톡 template code 입니다. 자세한 설명은 http://www.coolsms.co.kr/AboutAlimTalk을 참조해주세요. 

    # 알림톡에서 메시지내용은 Template Code에 맞는 메시지 내용이어야 하며 '#{홍길동}'과 같은 변수들은 다른 String으로 대체가 가능합니다.
    params['text'] = '#{홍길동}님이 #{게시판}에 새로운 게시물을 등록하였습니다.' 

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
