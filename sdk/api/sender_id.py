# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk.exceptions import CoolsmsException
from sdk.exceptions import CoolsmsSDKException
from sdk.exceptions import CoolsmsSystemException
from sdk.exceptions import CoolsmsServerException

## @class SenderID
#  @brief management sender id, using Rest API
class SenderID:
    # Coolsms Object
    cool = None

    ## @brief initialize
    #  @param string api_key [required]
    #  @param string api_secret [required]
    def __init__(self, api_key, api_secret):
        self.cool = Coolsms(api_key, api_secret)

        # set api name and version
        self.cool.set_api_config('senderid', '1.1')

    #  @brief sender id registration request ( HTTP Method POST )
    #  @param string phone [required]
    #  @param string site_user [optional]
    #  @return JSONObject
    def register(self, phone, site_user=None):
        if phone == None:
            raise CoolsmsSDKException("'phone' is required", 201);

        params = dict()
        params = {'phone':phone}
        if site_user:
            params['site_user'] = site_user

        response = self.cool.request_post('register', params)

        return response

    #  @brief verify sender id ( HTTP Method POST )
    #  @param string handle_key[required]
    #  @return None 
    def verify(self, handle_key):
        if handle_key == None:
            raise CoolsmsSDKException("'handle_key' is required", 201);

        params = dict()
        params = {'handle_key':handle_key}
        response = self.cool.request_post('verify', params)

        return response

    #  @brief delete sender id ( HTTP Method POST )
    #  @param string handle_key [required]
    #  @return None 
    def delete(self, handle_key):
        if handle_key == None:
            raise CoolsmsSDKException("'handle_key' is required", 201);

        params = dict()
        params = {'handle_key':handle_key}
        response = self.cool.request_post('delete', params)

        return response

    #  @brief get sender id list ( HTTP Method GET )
    #  @param string site_user [optional]
    #  @return JSONObject 
    def get_list(self, site_user=None):
        params = dict()

        if site_user:
            params = {'site_user':site_user}

        response = self.cool.request_get('list', params)
        return response

    #  @brief set default sender id ( HTTP Method POST )
    #  @param string handle_key [required]
    #  @param string site_user [optional]
    #  @return None
    def set_default(self, handle_key, site_user=None):
        if handle_key == None:
            raise CoolsmsSDKException("'handle_key' is required", 201);

        params = dict()
        params = {'handle_key':handle_key}

        if site_user:
            params['site_user'] = site_user

        response = self.cool.request_post('set_default', params)

        return response

    #  @brief get default sender id ( HTTP Method GET )
    #  @param string site_user [optional]
    #  @return JSONObject
    def get_default(self, site_user=None):
        params = dict()

        if site_user:
            params = {'site_user':site_user}

        response = self.cool.request_get('get_default', params)

        return response
