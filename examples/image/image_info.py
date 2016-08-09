# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.image import Image
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to check image info through CoolSMS Rest API
if __name__ == "__main__":

    # set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    image_id = "IMG57A42896DF7B0"
    cool = Image(api_key, api_secret)

    try:
        response = cool.get_image_info(image_id)
        print("Image_id : %s" % response['image_id'])
        print("File_name : %s" % response['file_name'])
        print("Original_name : %s" % response['original_name'])
        print("File_size : %s" % response['file_size'])
        print("Width : %s" % response['width'])
        print("Height : %s" % response['height'])
        
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
