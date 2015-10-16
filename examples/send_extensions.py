# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2015 NURIGO
 http://www.coolsms.co.kr
"""
import sys,json
sys.path.append("..")
import coolsms

def main():
	# API Credential 정보
	# https://www.coolsms.co.kr/index.php?mid=service_setup&act=dispSmsconfigCredentials
	api_key = 'NCS52A57F48C3D32'
	api_secret = '5AC44E03CE8E7212D9D1AD9091FA9966'

	# 수신번호
	to = '01000000000,01011111111' # <--- input comma-separated numbers

	# 발신번호
	# 2015/10/16 발신번호 등록제 시행에 따라 사전에 등록된 발신번호만 허용
	# http://www.coolsms.co.kr/index.php?mid=service_setup&act=dispSmsconfigSenderNumbers
	sender = '01012345678'

	# 메시지 내용
	message = '테스트 메시지'

	# JSON형식의 extension 데이터
	# 위에서 정의된 to, sender, message 등 기본 데이터를 상속받아 개별 메시지로 발송된다.
	data = [ {"to":"01000000001", "text":"Hello A"}, {"to":"01000000002", "text":"Hello B"} ]
	extension = json.dumps(data)

	# API Key, API Secret, App Version
	cool = coolsms.rest(api_key, api_secret, 'Example 1.0')
	status = cool.send(to,message,sender,extension=extension)

	# 리턴값 출력
	print status

	# 리턴값이 False이면 오류
	if status == False:
		print "ERROR: %s" % cool.get_error()

if __name__ == "__main__":
	main()
	sys.exit(0)
