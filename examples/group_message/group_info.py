# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.group_message import GroupMessage
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to check group info through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # group_id is mandatory.
    group_id = "GID57A82D462CBBF"

    cool = GroupMessage(api_key, api_secret)

    try:
        response = cool.get_group_info(group_id)
        print("Group ID : %s" % response['group_id'])
        print("Message Count : %s" % response['message_count'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
