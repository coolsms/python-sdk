# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
import base64
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk.exceptions import CoolsmsException
from sdk.exceptions import CoolsmsSDKException
from sdk.exceptions import CoolsmsSystemException
from sdk.exceptions import CoolsmsServerException

## @class Image 
#  @brief management image, using Rest API
class Image:
    # Coolsms Object
    cool = None

    ## @brief initialize
    #  @param string api_key [required]
    #  @param string api_secret [required]
    #  @param boolean use_http_connection [optional]
    #  @throws CoolsmsException
    def __init__(self, api_key, api_secret, use_http_connection = False):
        self.cool = Coolsms(api_key, api_secret)

        # if True. use http connection
        if use_http_connection == True:
            self.cool.use_http_connection()

    ## @brief get image list( HTTP Method GET )
    #  @param string offset [optional] [default:"0"]
    #  @param string limit [optional] [default:"20"]
    #  @return JSONObject
    #  @throws CoolsmsException
    def get_image_list(self, offset=None, limit=None):
        params = dict()

        if offset:
            params['offset'] = offset
        if limit:
            params['limit'] = limit

        response = self.cool.request_get('image_list', params)

        return response

    ## @brief get image info ( HTTP Method GET )
    #  @param string image_id [required]
    #  @return JSONObject
    #  @throws CoolsmsException
    def get_image_info(self, image_id):
        if image_id == None:
            raise CoolsmsSDKException("'image_id' is required", 201);

        resource = "images/" + image_id;
        response = self.cool.request_get(resource)

        return response

    ## @brief upload image ( HTTP Method POST )
    #  @param string image [required]
    #  @return JSONobject
    #  @throws CoolsmsException
    def upload_image(self, image):
        if image == None:
            raise CoolsmsSDKException("'image' is required", 201);

        params = dict()
        params = {'image':image}
        params['image_encoding'] = 'base64'

        files = {}
        try:
            with open(image, 'rb') as content_file:
                content = base64.b64encode(content_file.read())
                content = content.decode()
        except Exception as e:
            raise CoolsmsSystemException(e, 399)
        files = {'image': {'filename': image, 'content': content}}

        response = self.cool.request_post_multipart("upload_image", params, files)

        return response

    ## @brief delete images ( HTTP Method POST )
    #  @param string image_ids [required]
    #  @return JSONObject 
    #  @throws CoolsmsException
    def delete_images(self, image_ids):
        if image_ids == None:
            raise CoolsmsSDKException("'image_ids' is required", 201);
        
        params = dict()
        params = {'image_ids':image_ids}
        response = self.cool.request_post('delete_images', params)

        return response
