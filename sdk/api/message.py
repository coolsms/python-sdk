# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk import exceptions

#import sdk.coolsms

#from coolsms import coolsms

# class Message 
class Message:
    #
    def __init__(self, api_key, api_secret):
        Coolsms(api_key, api_secret)

    # access to send resource
    def send(params):
        if type(params) is not str:
            print("ERROR")
            #raise Exception("ERROR", "TT")

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
            A JSON type string will be returned. On failure, thorw Exception
        """

        # convert list to a comma seperated string
        if sys.version_info[0] == 2:
            t_temp = text.decode('utf-8')
            text = t_temp.encode('utf-8')
            text = unicode(text, encoding='utf-8')
        if type(to) == list:
            to = ','.join(to)

        if type:
            if type.lower() not in ['sms', 'lms', 'mms']:
                self.__set_error__('invalid message type')
                return False
        else:
            type = self.get_type()

        os_platform = platform.system()
        dev_lang = "Python %s" % platform.python_version()
        sdk_version = "sms-python %s" % __version__
        if app_version:
            self.app_version = app_version

        # get authentication info.
        timestamp, salt, signature = self.__get_signature__()

        fields = {'api_key': self.api_key,
                  'timestamp': timestamp,
                  'salt': salt,
                  'signature': signature.hexdigest(),
                  'type': mtype,
                  'os_platform': os_platform,
                  'dev_lang': dev_lang,
                  'sdk_version': sdk_version,
                  'app_version': self.app_version}

        if self.test:
            fields['mode'] = 'test'
        if self.srk:
            fields['srk'] = self.srk
        if to:
            fields['to'] = to
        if text:
            fields['text'] = text
        if sender:
            fields['from'] = sender
        if subject:
            fields['subject'] = subject
        if datetime:
            fields['datetime'] = datetime
        if extension:
            fields['extension'] = extension
        if country:
            fields['country'] = country

        if image is None:
            image = self.imgfile

        if mtype.lower() == 'mms':
            if image is None:
                self.__set_error__('image file path input required')
                return False
            try:
                with open(image, 'rb') as content_file:
                    content = content_file.read()
            except IOError as e:
                self.__set_error__("I/O error({0}): {1}".format(e.errno, e.strerror))
                return False
            except:
                self.__set_error__("Unknown error")
                return False
            files = {'image': {'filename': image, 'content': content}}
        else:
            files = {}

        # request post multipart-form
        host = self.host + ':' + str(self.port)
        selector = "/sms/%s/send" % self.api_version

        try:
            status, reason, response = post_multipart(host, selector, fields, files)
        except Exception as e:
            print(e)
            self.__set_error__("could not connect to server")
            return False
        if status != 200:
            try:
                err = json.loads(response)
            except:
                self.__set_error__("%u:%s" % (status, reason))
                return False
            self.__set_error__("%s:%s" % (err['code'], reason))
            return False
        return json.loads(response)

    # access to sent resource
    def status(self, page=1, count=20, s_rcpt=None, s_start=None, s_end=None, mid=None):
        params = dict()
        if page:
            params['page'] = page
        if count:
            params['count'] = count
        if s_rcpt:
            params['s_rcpt'] = s_rcpt
        if s_start:
            params['s_start'] = s_start
        if s_end:
            params['s_end'] = s_end
        if mid:
            params['mid'] = mid
        response, obj = self.request_get('sent', params)
        return obj

    # access to status resource
    def line_status(self, count=1):
        params = dict()
        if count:
            params['count'] = count
        response, obj = self.request_get('status', params)
        return obj

    # access to balance resource
    def balance(self):
        response, obj = self.request_get('balance')
        return int(obj['cash']), int(obj['point'])

    # access to cancel resource
    def cancel(self, mid=None, gid=None):
        if mid is None and gid is None:
            return False

        params = dict()
        if mid:
            params['mid'] = mid
        if gid:
            params['gid'] = gid

        response, obj = self.request_post('cancel', params)
        if response.status == 200:
            return True
        return False
