# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.sender_id import SenderID 
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to delete sender number through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # handle_key is mandatory.
    handle_key = "SID57A8456ADD428"

    cool = SenderID(api_key, api_secret)

    try:
        response = cool.delete(handle_key)
        if response == None:
            print("Register Success")

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit() 
