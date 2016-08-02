# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

class CoolsmsException(Exception):
	pass

class CoolsmsSDKException(CoolsmsException):
	pass

class CoolsmsServerException(CoolsmsException):
	pass

class CoolsmsSystemException(CoolsmsException):
	pass
