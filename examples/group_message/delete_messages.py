# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.group_message import GroupMessage
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to delete messages through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # group_id, message_ids are mandatory.
    group_id = "GID57A82D462CBBF" # Group ID
    message_ids = "MID2738AWQIEQQ" # Message IDs "MID29EII1913,MID1839231REE ..."

    cool = GroupMessage(api_key, api_secret)

    try:
        response = cool.delete_messages(group_id, message_ids)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
