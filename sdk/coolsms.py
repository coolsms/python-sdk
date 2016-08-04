# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
import hmac
import mimetypes
import uuid
import json
import time
import platform

from hashlib import md5
from sdk.exceptions import CoolsmsException
from sdk.exceptions import CoolsmsSDKException
from sdk.exceptions import CoolsmsSystemException
from sdk.exceptions import CoolsmsServerException

# sys.version_info.major is available in python version 2.7
# use sys.version_info[0] for python 2.6
if sys.version_info[0] == 2:
    from httplib import HTTPSConnection
    from urllib import urlencode
else:
    from http.client import HTTPSConnection
    from urllib.parse import urlencode

## @mainpage PYTHON SDK
#  @section intro 소개
#      - 소개 : Coolsms REST API SDK FOR PYTHON
#      - 버전 : 2.0
#      - 설명 : Coolsms REST API 를 이용 보다 빠르고 안전하게 문자메시지를 보낼 수 있는 PYTHON으로 만들어진 SDK 입니다.
#  @section CreateInfo 작성 정보
#      - 작성자 : Nurigo
#      - 작성일 : 2016/05/13 * 
#  @section common 기타 정보
#      - 저작권 GPL v2
#      - Copyright (C) 2008-2016 NURIGO
#      - http://www.coolsms.co.kr

## @class Coolsms 
#  @brief Gateway access url : https://api.coolsms.co.kr/{api type}/{verson}/{resource name}
class Coolsms:
    # SDK Version
    sdk_version = "2.0"

    # API Version
    api_version = "2"

    # SMS Gateway address
    host = 'api.coolsms.co.kr'

    # use secure channel as default
    port = 443

    # API Key
    api_key = None

    # API Secret
    api_secret = None

    # API Name
    api_name = "sms"

    # error handle
    error_string = None

    ## @brief initialize
    #  @param string api_key [required]
    #  @param string api_secret [required]
    def __init__(self, api_key=str(), api_secret=str()):
        self.api_key = api_key
        self.api_secret = api_secret

    ## @brief get signature
    #  @return string salt, string timestamp, string signature
    def __get_signature__(self):
        salt = str(uuid.uuid1())
        timestamp = str(int(time.time()))
        data = timestamp + salt
        return timestamp, salt, hmac.new(self.api_secret.encode(), data.encode(), md5)

    ## @brief http GET method request 
    #  @param string resource [required]
    #  @param dictionary params [optional]
    #  @return JSONObject
    def request_get(self, resource, params=None):
        if params == None:
            params = dict()

        params = self.set_base_params(params)
        params_str = urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   "User-Agent": "sms-python"}
        conn = HTTPSConnection(self.host, self.port)
        conn.request("GET", "/%s/%s/%s?" % (self.api_name, self.api_version, resource) + params_str, None, headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        # https status code is not 200, raise Exception
        if response.status != 200:
            error_msg = response.reason
            if(data):
                error_msg = data
            
            raise CoolsmsServerException(error_msg, response.status)

        # response data parsing
        obj = None
        if data:
            obj = json.loads(data)

        return obj

    ## @brief http POST method request 
    #  @param string resource [required]
    #  @param dictionary params [optional]
    #  @return JSONObject
    def request_post(self, resource, params=None):
        if params == None:
            params = dict()

        params = self.set_base_params(params)
        params_str = urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   "User-Agent": "sms-python"}
        conn = HTTPSConnection(self.host, self.port)
        conn.request("POST", "/%s/%s/%s" % (self.api_name, self.api_version, resource), params_str, headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        # https status code is not 200, raise Exception
        if response.status != 200:
            error_msg = response.reason
            if(data):
                error_msg = data
            
            raise CoolsmsServerException(error_msg, response.status)

        obj = None
        if data:
            obj = json.loads(data)

        return obj

    ## @brief http POST method multipart form request 
    #  @param string resource [required]
    #  @param dictionary params [optional]
    #  @param dictionary files [optional]
    #  @return JSONObject
    def request_post_multipart(self, resource, params, files):
        host = self.host + ':' + str(self.port)
        selector = "/%s/%s/%s" % (self.api_name, self.api_version, resource)

        params = self.set_base_params(params)
        content_type, body = self.encode_multipart_formdata(params, files)
        conn = HTTPSConnection(host)
        conn.putrequest('POST', selector)
        conn.putheader('content-type', content_type)
        conn.putheader('content-length', str(len(body)))
        conn.putheader('User-Agent', 'sms-python')
        conn.endheaders()
        conn.send(body)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        # https status code is not 200, raise Exception
        if response.status != 200:
            error_msg = response.reason
            if(data):
                error_msg = data
            
            raise CoolsmsServerException(error_msg, response.status)

        # response data parsing
        obj = None
        if data:
            obj = json.loads(data)

        return obj

    ## @brief format multipart form
    #  @param dictionary params [required]
    #  @param dictionary files [required]
    #  @return string content_type, string body
    def encode_multipart_formdata(self, params, files):
        boundary = str(uuid.uuid1())
        crlf = '\r\n'
        l = []
        for key, value in params.items():
            l.append('--' + boundary)
            l.append('Content-Disposition: form-data; name="%s"' % key)
            l.append('')
            l.append(value)

        for key, value in files.items():

            print(self.get_content_type(value['filename']))
            l.append('--' + boundary)
            l.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, value['filename']))
            l.append('Content-Type: %s' % self.get_content_type(value['filename']))

            print(type(value['content']))
            l.append('')
            l.append(str(value['content']))

        l.append('--' + boundary + '--')
        l.append('')
        
        body = crlf.join(l).encode('utf-8')
        """
        body = body.encode('utf-8')

        print("WOW")
        for key, value in files.items():
            print(self.get_content_type(value['filename']))
            image_data = '--' + boundary + crlf
            image_data += 'Content-Type: %s' % self.get_content_type(value['filename']) + crlf
            image_data += 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, value['filename']) + crlf
            image_data += crlf
            image_data = image_data.encode('utf-8')

            body += image_data
            body += value['content']

        end_data = crlf + '--' + boundary + '--' + crlf
        end_data += crlf
        end_data = end_data.encode('utf-8')
        body += end_data
        """

        content_type = 'multipart/form-data; boundary=%s' % boundary

        return content_type, body    
    
    ## @brief get content type
    #  @param string filesname [required]
    #  @return string content_type
    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    ## @brief set base parameter
    #  @param dictionary params [required]
    #  @return dictionary params
    def set_base_params(self, params):
        timestamp, salt, signature = self.__get_signature__()
        base_params = {'api_key': self.api_key, 'timestamp': timestamp, 'salt': salt,
                       'signature': signature.hexdigest()}
        params.update(base_params)
        return params

    ## @brief check send data
    #  @param dictionary params [required]
    #  @return dictionary params
    def check_send_data(params):
        # require fields check
        if all (k in params for k in ("to", "from", "text")) == False:
            raise CoolsmsSDKException("parameter 'to', 'from', 'text' are required", 201)

        for key, val in params.items():
            print("Code : {0}, Value : {1}".format(key, val))

            if key == "text" and sys.version_info[0] == 2:
                text = val
                t_temp = text.decode('utf-8')
                text = t_temp.encode('utf-8')
                text = unicode(text, encoding='utf-8')
                params['text'] = text

            # convert list to a comma seperated string
            if key == "to" and val == list:
                params['to'] = ','.join(to)

            # message type check
            if key == "type" and val.lower() not in ['sms', 'lms', 'mms', 'ata']:
                raise CoolsmsSDKException("message type is not supported", 201)

        return params

    ## @brief set api name and api version
    #  @param string api_name [required] 'sms', 'senderid', 'image'
    #  @param integer api_version [required]
    def set_api_config(self, api_name, api_version):
        self.api_name = api_name;
        self.api_version = api_version;
