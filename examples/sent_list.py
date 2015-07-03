# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2014 NURIGO
 http://www.coolsms.co.kr
"""
import sys
sys.path.append("..")
import coolsms

def main():
	api_key = 'NCS52A57F48C3D32'
	api_secret = '5AC44E03CE8E7212D9D1AD9091FA9966'
	cool = coolsms.rest(api_key, api_secret)
	status = cool.status()
	print status

if __name__ == "__main__":
	main()
	sys.exit(0)
