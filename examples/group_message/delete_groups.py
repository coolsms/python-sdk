# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.group_message import GroupMessage
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to delete sms group through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # group_ids is mandatory
    group_ids = "GID57A82D462CBBFF" # Group IDs "GID57A82D462CBBFF,GID98A82D462CDBFF ..."

    cool = GroupMessage(api_key, api_secret)

    try:
        response = cool.delete_groups(group_ids)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])

        if response['error_list']:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
