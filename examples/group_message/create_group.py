# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.group_message import GroupMessage
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to create sms group through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # Optional parameters for your own needs
    params = dict()
    # params["charset"] = "utf8" # utf8, euckr default value is utf8
    # params["srk"] = "293DIWNEK103" # Solution key
    # params["mode"] = "test" # If 'test' value, refund cash to point
    # params["only_ata"] = "true" # If 'true' value, only send ata
    # params["delay"] = "10" # '0~20' delay messages
    # params["force_sms"] = "true"; # true is always send sms ( default true )
    # params["app_version"] = "" # A version

    cool = GroupMessage(api_key, api_secret)

    try:
        response = cool.create_group(params)
        print("Group ID : %s" % response['group_id'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
