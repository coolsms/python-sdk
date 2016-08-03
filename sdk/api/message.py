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

# class Message 
class Message:
    cool = None

    # initialize
    def __init__(self, api_key, api_secret):
        self.cool = Coolsms(api_key, api_secret)

    # access to send resource
    def send(self, params):
        """Request to REST API server to send SMS messages

        Arguments:
            to : A comma seperated string which contains phone numbers.
            from : sender number
            text : Message content
            type : one of sms, lms, mms
            template_code : alimtalk template code
            sender_key : alimtalk sender key
            subject : If you send LMS or MMS, you should input the subject of the message(s).
            image : Include image, when you send MMS.
            datetime : Use this field when you send scheduled messages.
            country : country code ( korea:82, japan:81 ... visit 'http://countrycode.org' )
            
            and more informations, visit 'http://www.coolsms.co.kr/SMS_API_v2#POSTsend'

        Returns:
            A JSON type string will be returned. On failure, raise Exception
        """
        # params type check
        if type(params) is not dict:
            raise CoolsmsSDKException("parameter type is not dictionary", 201)

        # require fields check
        if all (k in params for k in ("to", "from", "text")) == False:
            raise CoolsmsSDKException("parameter 'to', 'from', 'text' is required", 201)

        for key, val in params.items():
            print("Code : {0}, Value : {1}".format(key, val))

            if key == "text" and sys.version_info[0] == 2:
                t_temp = text.decode('utf-8')
                text = t_temp.encode('utf-8')
                text = unicode(text, encoding='utf-8')
                params['text'] = text

            # convert list to a comma seperated string
            if key == "to" and val == list:
                to = ','.join(to)

            # message type check
            if key == "type" and val.lower() not in ['sms', 'lms', 'mms', 'ata']:
                raise CoolsmsSDKException("message type is not supported", 201)

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

    # access to statusresource
    def status(self, params=None):
        response = self.cool.request_get('status', params)
        return response 

    # access to status resource
    def sent(self, params=None):
        response = self.cool.request_get('sent', params)
        return response 

    # access to balance resource
    def balance(self):
        response = self.cool.request_get('balance')
        return response

    # access to cancel resource
    def cancel(self, params):
        if 'message_id' not in params and 'group_id' not in params:
            raise CoolsmsSDKException("message_id or group_id either one must be entered", 202)

        response = self.cool.request_post('cancel', params)
        return response
