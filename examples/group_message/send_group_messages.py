# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
# python 2.7 일 경우 사용
#reload(sys)
#sys.setdefaultencoding('utf-8')

sys.path.insert(0, "../../")

from sdk.api.group_message import GroupMessage
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to add messages into group through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = '#ENTER_YOUR_OWN#'
    api_secret = '#ENTER_YOUR_OWN#'

    cool = GroupMessage(api_key, api_secret)
    group_id = None

    # 그룹생성
    params = dict()
    params['app_version'] = 'TestApp v1.0'
    try:
        response = cool.create_group(params)
        group_id = response['group_id']
        print("Group ID : %s" % group_id)
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
        sys.exit()

    # 메시지추가
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = '01000000001' # Recipients Number '01000000000,01000000001'
    params['from'] = '01000000002' # Sender number
    params['text'] = '테스트 메시지' # Message
    params['group_id'] = group_id # Group ID
    try:
        response = cool.add_messages(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        if "error_list" in response:
            print("Error List : %s" % response['error_list'])
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
        sys.exit()

    # 발송
    try:
        response = cool.send(group_id)
        print("발송된 그룹ID : %s" % response['group_id'])
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
