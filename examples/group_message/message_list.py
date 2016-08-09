# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.group_message import GroupMessage
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate check message list through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # group_id is mandatory
    params = dict()
    params['group_id'] = "GID57A82D462CBBF" # Group ID
    # params["offset"] = "0" // default 0
    # params["limit"] = "20" // default 20

    cool = GroupMessage(api_key, api_secret)

    try:
        response = cool.get_message_list(params)
        print("Total Count : %s" % response['total_count'])
        print("Limit : %s" % response['limit'])
        print("Offset : %s" % response['offset'])
        print("List : %s" % response['list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
