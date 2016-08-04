# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk.exceptions import CoolsmsException
from sdk.exceptions import CoolsmsSDKException
from sdk.exceptions import CoolsmsSystemException
from sdk.exceptions import CoolsmsServerException

# class Image
class Image:
    #
    def __init__(self, api_key, api_secret):
        Coolsms(api_key, api_secret)

    # 
    def get_image_list(self):
        return

    # 
    def get_image_info(self):
        return

    # 
    def upload_image(self):
        return 

    # 
    def delete_images(self):
        return
