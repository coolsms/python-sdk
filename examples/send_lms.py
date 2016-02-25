# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2015 NURIGO
 http://www.coolsms.co.kr
"""
import sys
sys.path.append("..")
import coolsms

def main():
	# API Credential 정보
	# https://www.coolsms.co.kr/index.php?mid=service_setup&act=dispSmsconfigCredentials
	api_key = 'NCS52A57F48C3D32'
	api_secret = '5AC44E03CE8E7212D9D1AD9091FA9966'

	# 수신번호
	to = '01000000000'

	# 발신번호
	# 2015/10/16 발신번호 등록제 시행에 따라 사전에 등록된 발신번호만 허용
	# http://www.coolsms.co.kr/index.php?mid=service_setup&act=dispSmsconfigSenderNumbers
	sender = '01012345678'

	# 메시지 내용
	message = 'LMS 2,000 바이트까지 입력가능합니다'

	# API Key, API Secret, App Version
	cool = coolsms.rest(api_key, api_secret, 'Example 1.0')

	# 메시지 발송 요청
	status = cool.send(to,message,sender,mtype='lms',subject='LMS 제목(40바이트)')

	# 리턴값 출력
	print status

	# 리턴값이 False이면 오류
	if status == False:
		print cool.get_error()

if __name__ == "__main__":
	main()
	sys.exit(0)
