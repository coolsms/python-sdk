# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-
from hashlib import md5
import sys
import hmac
import mimetypes
import uuid
import json
import time
import platform

from sdk.exceptions import CoolsmsServerException

# sys.version_info.major is available in python version 2.7
# use sys.version_info[0] for python 2.6
if sys.version_info[0] == 2:
    from httplib import HTTPSConnection
    from urllib import urlencode
else:
    from http.client import HTTPSConnection
    from urllib.parse import urlencode
"""
 Copyright (C) 2008-2016 NURIGO
 http://www.coolsms.co.kr
"""

# class Coolsms 
# Gateway access url : https://api.coolsms.co.kr/{api type}/{verson}/{resource name}
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

    # error handle
    error_string = None

    # constructor
    def __init__(self, api_key=str(), api_secret=str()):
        self.api_key = api_key
        self.api_secret = api_secret

    # return salt, timestamp, signature
    def __get_signature__(self):
        salt = str(uuid.uuid1())
        timestamp = str(int(time.time()))
        data = timestamp + salt
        return timestamp, salt, hmac.new(self.api_secret.encode(), data.encode(), md5)

    # error handle
    def __set_error__(self, error_str):
        self.error_string = error_str

    # return error string set
    def get_error(self):
        return self.error_string

    # http GET request 
    def request_get(self, resource, params=None):
        if params == None:
            params = dict()

        params = self.set_base_params(params)
        params_str = urlencode(base_params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   "User-Agent": "sms-python"}
        conn = HTTPSConnection(self.host, self.port)
        conn.request("GET", "/sms/%s/%s?" % (self.api_version, resource) + params_str, None, headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        # https status code is not 200, raise Exception
        if response.status != 200:
            raise CoolsmsServerException(response.reason, response.status)

        # response data parsing
        obj = None
        if data:
            obj = json.loads(data)

        return obj

    # http POST request
    def request_post(self, resource, params=None):
        if params == None:
            params = dict()

        params = self.set_base_params(params)
        params_str = urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   "User-Agent": "sms-python"}
        conn = HTTPSConnection(self.host, self.port)
        conn.request("POST", "/sms/%s/%s" % (self.api_version, resource), params_str, headers)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        # https status code is not 200, raise Exception
        if response.status != 200:
            raise CoolsmsServerException(response.reason, response.status)

        obj = None
        if data:
            obj = json.loads(data)

        return obj

    # send multipart form to the server
    def request_post_multipart(self, resource, params, files):
        host = self.host + ':' + str(self.port)
        selector = "/sms/%s/%s" % (self.api_version, resource)

        params = self.set_base_params(params)
        content_type, body = self.encode_multipart_formdata(params, files)
        conn = HTTPSConnection(host)
        conn.putrequest('POST', selector)
        conn.putheader('content-type', content_type)
        conn.putheader('content-length', str(len(body.encode('utf-8'))))
        conn.putheader('User-Agent', 'sms-python')
        conn.endheaders()
        conn.send(body.encode('utf-8'))
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        # https status code is not 200, raise Exception
        if response.status != 200:
            raise CoolsmsServerException(response.reason, response.status)

        # response data parsing
        obj = None
        if data:
            obj = json.loads(data)

        return obj

    # format multipart form
    def encode_multipart_formdata(self, fields, files):
        boundary = str(uuid.uuid1())
        crlf = '\r\n'
        l = []
        for key, value in fields.items():
            l.append('--' + boundary)
            l.append('Content-Disposition: form-data; name="%s"' % key)
            l.append('')
            l.append(value)
        l.append('')
        body = crlf.join(l)
        for key, value in files.items():
            body += '--' + boundary + crlf
            body += 'Content-Type: %s' % get_content_type(value['filename']) + crlf
            body += 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, value['filename']) + crlf
            body += crlf
            body = body.encode('utf-8') + value['content'] + crlf
        body += '--' + boundary + '--' + crlf
        body += crlf
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body    
    
    # get content type
    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    # set base parameter
    def set_base_params(self, params):
        timestamp, salt, signature = self.__get_signature__()
        base_params = {'api_key': self.api_key, 'timestamp': timestamp, 'salt': salt,
                       'signature': signature.hexdigest()}
        params.update(base_params)
        return params
