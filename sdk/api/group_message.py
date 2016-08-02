# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk import exceptions

# class GroupMessage
class GroupMessage:
    #
    def __init__(self, api_key, api_secret):
        Coolsms(api_key, api_secret)

    # 
    def create_group(self):
        return

    # 
    def get_group_list(self):
        return

    # 
    def delete_groups(self):
        return 

    # 
    def get_group_info(self):
        return

    #
    def add_messages(self):
        return

    #
    def add_messages_json(self):
        return

    #
    def delete_messages(self):
        return

    #
    def send(self):
        return
