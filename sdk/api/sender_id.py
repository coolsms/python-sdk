# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk import exceptions

# class SenderId
class SenderId:
    #
    def __init__(self, api_key, api_secret):
        Coolsms(api_key, api_secret)

    # 
    def register(self):
        return

    # 
    def verify(self):
        return

    # 
    def delete(self):
        return 

    # 
    def get_list(self):
        return

    #
    def set_default(self):
        return

    #
    def get_default(self):
        return
