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
        timestamp, salt, signature = self.__get_signature__()
        base_params = {'api_key': self.api_key, 'timestamp': timestamp,
                       'salt': salt, 'signature': signature.hexdigest()}
        if params:
            base_params.update(params.items())
        params_str = urlencode(base_params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   "User-Agent": "sms-python"}
        conn = HTTPSConnection(self.host, self.port)
        conn.request("GET", "/sms/%s/%s?" % (self.api_version, resource) + params_str, None, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        obj = response, json.loads(data)
        return obj

    # http POST request
    def request_post(self, resource, params=None):
        timestamp, salt, signature = self.__get_signature__()
        base_params = {'api_key': self.api_key, 'timestamp': timestamp, 'salt': salt,
                       'signature': signature.hexdigest()}
        if params:
            base_params.update(params)
        params_str = urlencode(base_params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   "User-Agent": "sms-python"}
        conn = HTTPSConnection(self.host, self.port)
        conn.request("POST", "/sms/%s/%s" % (self.api_version, resource), params_str, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        json_obj = None
        if data:
            json_obj = json.loads(data)
        return response, json_obj

    # send multipart form to the server
    def request_post_multipart(host, selector, fields, files):
        content_type, body = encode_multipart_formdata(fields, files)
        h = HTTPSConnection(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body.encode('utf-8'))))
        h.putheader('User-Agent', 'sms-python')
        h.endheaders()
        h.send(body.encode('utf-8'))
        resp = h.getresponse()
        return resp.status, resp. reason, resp.read().decode()

    # format multipart form
    def encode_multipart_formdata(fields, files):
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
