# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
import platform
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk.exceptions import CoolsmsException
from sdk.exceptions import CoolsmsSDKException
from sdk.exceptions import CoolsmsSystemException
from sdk.exceptions import CoolsmsServerException

## @class Message 
#  @brief management message, using Rest API
class Message:
    # Coolsms Object
    cool = None

    ## @brief initialize
    #  @param string api_key [required]
    #  @param string api_secret [required]
    def __init__(self, api_key, api_secret):
        self.cool = Coolsms(api_key, api_secret)

    ## @brief send messages ( HTTP Method POST )
    #  @param dictionary params {
    #  @param string to [required]
    #  @param string from [required]
    #  @param string text [required]
    #  @param string type [optional]
    #  @param mixed image [optional]
    #  @param string image_encoding [optional]
    #  @param string refname [optional]
    #  @param mixed country [optional]
    #  @param string datetime [optional]
    #  @param string subject [optional]
    #  @param string charset [optional]
    #  @param string srk [optional]
    #  @param string mode [optional]
    #  @param string extension [optional]
    #  @param integer delay [optional]
    #  @param boolean force_sms [optional]
    #  @param string app_version [optional] }
    #  @return JSONObject
    def send(self, params):
        # params type check
        if type(params) is not dict:
            raise CoolsmsSDKException("parameter type is not dictionary", 201)

        params = Coolsms.check_send_data(params)

        # system info
        params['os_platform'] = platform.system()
        params['dev_lang'] = "Python %s" % platform.python_version()
        params['sdk_version'] = "sms-python %s" % Coolsms.sdk_version

        # type이 mms일때 image file check
        files = {}
        if 'type' in params and params['type'] == 'mms':
            if params['image'] is None:
                raise CoolsmsSDKException('image file is required')

            try:
                with open(params['image'], 'rb') as content_file:
                    content = content_file.read()
            except Exception as e:
                raise CoolsmsSystemException(e, 399)

            files = {'image': {'filename': image, 'content': content}}

        # request post multipart-form
        response = self.cool.request_post_multipart("send", params, files)
        return response

    ## @brief get status ( HTTP Method GET )
    #  @param dictionary params {
    #  @param integer count [optional]
    #  @param string unit [optional]
    #  @param string date [optional]
    #  @param integer channel [optional] }
    #  @return JSONObject
    #  @throws CoolsmsException
    def status(self, params=None):
        response = self.cool.request_get('status', params)
        return response 

    ## @brief sent messages ( HTTP Method GET )
    #  @param dictionary params {
    #  @param integer offset [optional]
    #  @param integer limit [optional]
    #  @param string rcpt [optional]
    #  @param string start [optional]
    #  @param string end [optional]
    #  @param string status [optional]
    #  @param string status [optional]
    #  @param string resultcode [optional]
    #  @param string notin_resultcode [optional]
    #  @param string message_id [optional]
    #  @param string group_id [optional] }
    #  @return JSONObject
    def sent(self, params=None):
        response = self.cool.request_get('sent', params)
        return response 

    ## @brief get remaining balance ( HTTP Method GET )
    #  @param None
    #  @return JSONobject
    def balance(self):
        response = self.cool.request_get('balance')
        return response

    ## @brief cancel reserve message. mid or gid either one must be entered. ( HTTP Method POST )
    #  @param dictionary params {
    #  @param string mid [optional]
    #  @param string gid [optional] }
    #  @return None
    def cancel(self, params):
        if 'message_id' not in params and 'group_id' not in params:
            raise CoolsmsSDKException("message_id or group_id either one must be entered", 201)

        response = self.cool.request_post('cancel', params)
        return response
