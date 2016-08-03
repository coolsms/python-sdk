# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

class CoolsmsException(Exception):
    def __init__(self, message, code):
        self.code = code
        self.msg = message

class CoolsmsSDKException(CoolsmsException):
	pass

class CoolsmsServerException(CoolsmsException):
	pass

class CoolsmsSystemException(CoolsmsException):
	pass
