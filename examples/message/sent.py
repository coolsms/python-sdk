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

    # 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    # params["messaage_id"] = "M52CB443257C61" # message id
    # params["group_id"] = "G52CB4432576C8" # group id
    # params["offset"] = "0" # default 0
    # params["limit"] = "1" # default 20
    # params["rcpt"] = "01000000000" # search sent result by recipient number 
    # params["start"] = "201601070915" # set search start date 
    # params["end"] = "201601071230" # set search end date

    cool = Message(api_key, api_secret)
    try:
        i = 0
        response = cool.sent(params)
        for data in response['data']:
            i += 1
            print("Message No.%s" % i)
            print("Type : %s" % data['type'])
            print("Accepted_time : %s" % data['accepted_time'])
            print("Recipient_number : %s" % data['recipient_number'])
            print("Group_id : %s" % data['group_id'])
            print("Message_id : %s" % data['message_id'])
            print("Status : %s" % data['status'])
            print("Result_code : %s" % data['result_code'])
            print("Result_message : %s" % data['result_message'])
            print("Sent_time : %s" % data['sent_time'])
            print("Text : %s" % data['text'])
            print("Carrier : %s" % data['carrier'])
            print("Scheduled_time : %s" % data['scheduled_time'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
