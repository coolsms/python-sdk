# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2015 NURIGO
 http://www.coolsms.co.kr
"""
import sys
sys.path.append("..")
import coolsms

def main():
	api_key = 'NCS52A57F48C3D32'
	api_secret = '5AC44E03CE8E7212D9D1AD9091FA9966'
	to = '01000000000'
	sender = '01012345678'
	message = 'MMS 2,000 바이트까지 입력가능합니다'
	cool = coolsms.rest(api_key, api_secret, 'Example 1.0')
	status = cool.send(to,message,sender,mtype='mms',subject='MMS 제목(40바이트)',image='test.jpg')
	if status == False:
		print cool.get_error()
	print status

if __name__ == "__main__":
	main()
	sys.exit(0)
