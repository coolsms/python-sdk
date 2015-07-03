# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2015 NURIGO
 http://www.coolsms.co.kr
"""

__version__ = "1.1"

from hashlib import md5
import sys,httplib,urllib,hmac,mimetypes,uuid,json,time
import platform
# reload(sys) needs to use sys.setdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

# send multipart form to the server
def post_multipart(host, selector, fields, files):
	content_type, body = encode_multipart_formdata(fields, files)
	h = httplib.HTTPS(host)
	h.putrequest('POST', selector)
	h.putheader('content-type', content_type)
	h.putheader('content-length', str(len(body)))
	h.putheader('User-Agent', 'sms-python')
	h.endheaders()
	h.send(body)
	errcode, errmsg, headers = h.getreply()
	return errcode, errmsg, h.file.read()

# format multipart form
def encode_multipart_formdata(fields, files):
	BOUNDARY = str(uuid.uuid1())
	CRLF = '\r\n'
	L = []
	for key, value in fields.items():
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"' % key)
		L.append('')
		L.append(value)
	L.append('')
	body = CRLF.join(L)
	for key, value in files.items():
		body = body + '--' + BOUNDARY + CRLF
		body = body + 'Content-Type: %s' % get_content_type(value['filename']) + CRLF
		body = body + 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, value['filename']) + CRLF
		body = body + CRLF
		body = body.encode('utf-8') + value['content'] + CRLF
	body = body + '--' + BOUNDARY + '--' + CRLF
	body = body + CRLF
	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
	return content_type, body

def get_content_type(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

# class rest
# SMS Gateway access url : https://api.coolsms.co.kr/{verson}/{resource name}
class rest:
	# SMS Gateway address
	host = 'api.coolsms.co.kr'

	# use secure channel as default
	port = 443

	# api version
	api_version = '1.5'

	# API Key
	api_key = None

	# API Secret
	api_secret = None

	# solution registration key
	srk = None

	# message type (sms, lms, mms)
	mtype = 'sms'

	# image file
	imgfile = None

	# error handle
	error_string = None

	# TRUE : test mode
	test = False

	# application version
	app_version = 'APP 1.0'

	# constructor
	def __init__(self, api_key, api_secret, app_version = None, srk = None, test = False, api_version = None):
		self.api_key = api_key
		self.api_secret = api_secret
		self.srk = srk
		if app_version:
			self.app_version = app_version
		self.test = test
		if api_version:
			self.api_version = api_version

	# return salt, timestamp, signature
	def __get_signature__(self):
		salt = str(uuid.uuid1())
		timestamp = str(int(time.time()))
		data = timestamp + salt
		return timestamp, salt, hmac.new(self.api_secret, data, md5)

	# error handle
	def __set_error__(self, error_str):
		self.error_string = error_str

	# return message type set
	def get_type(self):
		return self.mtype

	# return error string set
	def get_error(self):
		return self.error_string

	# set one of sms , lms , mms
	def set_type(self, mtype):
		if mtype.lower() not in ['sms','lms','mms']:
			return False
		self.mtype = mtype.lower()
		return True

	# set image file path
	def set_image(self, image):
		self.imgfile = image

	# access to send resource
	def send(self, to=None, text=None, sender=None, mtype=None, subject=None, image=None, datetime=None, extension=None, app_version=None):
		"""Request to REST API server to send SMS messages

		Arguments:
			to : A comma seperated string which contains phone numbers.
			text : Message content
			sender : sender id
			mtype : one of sms, lms, mms
			subject : If you send LMS or MMS, you should input the subject of the message(s).
			image : Include image, when you send MMS.
			datetime : Use this field when you send scheduled messages.
			extension : JSON formatted string. Please refer to API document.
			app_version : You'd better set this field as your own application's name. It's useful when you need any helf from COOLSMS service center.

		Returns:
			A JSON type string will be returned. On failure, False will be returned.
		"""
		# convert list to a comma seperated string
		if type(to) == list:
			to = ','.join(to)

		if mtype:
			if mtype.lower() not in ['sms','lms','mms']:
				self.__set_error__('invalid message type')
				return False
		else:
			mtype = self.get_type()

		os_platform = platform.system()
		dev_lang = "Python %s" % platform.python_version()
		sdk_version = "sms-python %s" % __version__
		if app_version:
			self.app_version = app_version

		# get authentication info.
		timestamp, salt, signature = self.__get_signature__()

		fields = {'api_key':self.api_key
					, 'timestamp':timestamp
					, 'salt':salt
					, 'signature':signature.hexdigest()
					, 'type':mtype
					, 'os_platform':os_platform
					, 'dev_lang':dev_lang
					, 'sdk_version':sdk_version
					, 'app_version':self.app_version}
		if self.test:
			fields['mode'] = 'test'
		if self.srk != None:
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

		if image == None:
			image = self.imgfile

		if mtype.lower() == 'mms':
			if image == None:
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
			files = {'image':{'filename':image,'content':content}}
		else:
			files = {}

		# request post multipart-form
		host = self.host + ':' + str(self.port)
		selector = "/sms/%s/send" % self.api_version

		try:
			status, reason, response = post_multipart(host, selector, fields, files)
		except:
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
	def status(self, page = 1, count = 20, s_rcpt = None, s_start = None, s_end = None, mid = None):
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
	def line_status(self, count = 1):
		params = dict()
		if count:
			params['count'] = count
		response, obj = self.request_get('status', params)
		return obj

	# access to balance resource
	def balance(self):
		timestamp, salt, signature = self.__get_signature__()
		response, obj = self.request_get('balance')
		return int(obj['cash']), int(obj['point'])

	# access to cancel resource
	def cancel(self, mid = None, gid = None):
		if mid == None and gid == None:
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

	def request_get(self, resource, params = None):
		timestamp, salt, signature = self.__get_signature__()
		base_params = {'api_key':self.api_key, 'timestamp':timestamp, 'salt':salt, 'signature':signature.hexdigest()}
		if params:
			base_params = dict(base_params.items() + params.items())
		params_str = urllib.urlencode(base_params)
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "sms-python"}
		conn = httplib.HTTPSConnection(self.host, self.port)
		conn.request("GET", "/sms/%s/%s?" % (self.api_version, resource) + params_str, None, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		obj = response, json.loads(data)
		return obj

	def request_post(self, resource, params = None):
		timestamp, salt, signature = self.__get_signature__()
		base_params = {'api_key':self.api_key, 'timestamp':timestamp, 'salt':salt, 'signature':signature.hexdigest()}
		if params:
			base_params = dict(base_params.items() + params.items())
		params_str = urllib.urlencode(base_params)
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "sms-python"}
		conn = httplib.HTTPSConnection(self.host, self.port)
		conn.request("POST", "/sms/%s/%s" % (self.api_version, resource), params_str, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		json_obj = None
		if data:
			json_obj = json.loads(data)
		return response, json_obj
