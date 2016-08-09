# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.sender_id import SenderID 
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to request sender number register through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    # phone is mandatory.
    phone = "01000000000"

    cool = SenderID(api_key, api_secret)

    try:
        response = cool.register(phone)
        print("ARS Number : %s" % response['ars_number'])
        print("Handle Key : %s" % response['handle_key'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
