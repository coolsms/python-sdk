# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2015 NURIGO
 http://www.coolsms.co.kr
"""
import sys,json
sys.path.append("..")
import coolsms

def main():
	api_key = 'NCS52A57F48C3D32'
	api_secret = '5AC44E03CE8E7212D9D1AD9091FA9966'
	to = '01000000000,01011111111' # <--- input comma-separated numbers
	sender = '01012345678'
	message = '테스트 메시지'
	data = [ {"to":"01000000001", "text":"Hello A"}, {"to":"01000000002", "text":"Hello B"} ]
	extension = json.dumps(data)
	cool = coolsms.rest(api_key, api_secret, 'Example 1.0')
	status = cool.send(to,message,sender,extension=extension)
	print status
	if status == False:
		print "ERROR: %s" % cool.get_error()

if __name__ == "__main__":
	main()
	sys.exit(0)
