# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
import platform
import base64
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
    #  @param boolean use_http_connection [optional]
    def __init__(self, api_key, api_secret, use_http_connection = False):
        self.cool = Coolsms(api_key, api_secret)

        # if True. use http connection
        if use_http_connection == True:
            self.cool.use_http_connection()

    ## @brief send messages ( HTTP Method POST )
    #  @param dictionary params {
    #  @param string to [required]
    #  @param string from [required]
    #  @param string text [required]
    #  @param string type [optional] [default:"sms"]
    #  @param mixed image [optional]
    #  @param string image_encoding [optional]
    #  @param string refname [optional]
    #  @param mixed country [optional] [default:"82"]
    #  @param string datetime [optional]
    #  @param string subject [optional]
    #  @param string charset [optional] [default:"utf8"]
    #  @param string srk [optional]
    #  @param string mode [optional]
    #  @param string extension [optional]
    #  @param integer delay [optional] [default:"0"]
    #  @param boolean force_sms [optional]
    #  @param string app_version [optional] 
    #  @param string template_code [optional] 
    #  @param string sender_key [optional] 
    #  @param string only_ata [optional] [default:"false"] }
    #  @return JSONObject
    #  @throws CoolsmsException
    def send(self, params):
        # params type check
        if type(params) is not dict:
            raise CoolsmsSDKException("parameter type is not dictionary", 201)

        params = self.cool.check_send_data(params)

        # system info
        params['os_platform'] = platform.system()
        params['dev_lang'] = "Python %s" % platform.python_version()
        params['sdk_version'] = "sms-python %s" % Coolsms.sdk_version

        # type이 mms일때 image file check
        files = {}
        if 'type' in params and params['type'] == 'mms':
            if 'image' not in params:
                raise CoolsmsSDKException('image file is required', 201)

            try:
                with open(params['image'], 'rb') as content_file:
                    content = base64.b64encode(content_file.read())
                    content = content.decode()
            except Exception as e:
                raise CoolsmsSystemException(e, 399)
            files = {'image': {'filename': params['image'], 'content': content}}
            params['image_encoding'] = 'base64'

        # request post multipart-form
        response = self.cool.request_post_multipart("send", params, files)
        return response

    ## @brief get status ( HTTP Method GET )
    #  @param dictionary params {
    #  @param integer count [optional] [default:"1"]
    #  @param string unit [optional]
    #  @param string date [optional] [default:현재시각]
    #  @param integer channel [optional] [default:"1"] }
    #  @return JSONObject
    #  @throws CoolsmsException
    def status(self, params=None):
        response = self.cool.request_get('status', params)
        return response 

    ## @brief sent messages ( HTTP Method GET )
    #  @param dictionary params {
    #  @param integer offset [optional]
    #  @param integer limit [optional] [default:"20"]
    #  @param string rcpt [optional]
    #  @param string start [optional]
    #  @param string end [optional]
    #  @param string status [optional]
    #  @param string status [optional]
    #  @param string resultcode [optional]
    #  @param string message_id [optional]
    #  @param string group_id [optional] }
    #  @return JSONObject
    #  @throws CoolsmsException
    def sent(self, params=None):
        response = self.cool.request_get('sent', params)
        return response 

    ## @brief get remaining balance ( HTTP Method GET )
    #  @param None
    #  @return JSONobject
    #  @throws CoolsmsException
    def balance(self):
        response = self.cool.request_get('balance')
        return response

    ## @brief cancel reserve message. mid or gid either one must be entered. ( HTTP Method POST )
    #  @param dictionary params {
    #  @param string mid [optional]
    #  @param string gid [optional] }
    #  @return None
    #  @throws CoolsmsException
    def cancel(self, params):
        if 'message_id' not in params and 'group_id' not in params:
            raise CoolsmsSDKException("message_id or group_id either one must be entered", 201)

        response = self.cool.request_post('cancel', params)
        return response
