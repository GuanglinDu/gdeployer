#!/usr/bin/env python
# coding:utf-8
# gdeployer configuration file gdeployer.ini parser
# Based on Phus Lu's Goagent uploader.py.
# Coded in Notepad++ (http://notepad-plus-plus.org/)
# Author:
#      Guanglin Du <guanglin.du@gmail.com>

import os
import re
import ConfigParser

# Versions based on date
__version__ = '20141001b'

# Class to read the configuration info.
class GDeployerConfigParser(object):
	def __init__(self):
		"""Read all the configuration info from file gdeployer.ini."""
		self.config = ConfigParser.RawConfigParser()
		self.config.read('gdeployer.ini')

		# appids,  goagent server src dir, Python interpretor & location of GAE appcfg.py
		self.appid = self.config.get('gae', 'appid')	
		self.goagent_server_src = self.config.get('gae', 'goagent_server_src')		
		self.python = self.config.get('gae', 'python')			
		self.gae_sdk_root = self.config.get('gae', 'gae_sdk_root')	

		# Email address & 2-step authentication
		self.with_email = self.config.get('authentication', 'with_email')
		self.email = self.config.get('authentication', 'email')
		self.auth2 = self.config.get('authentication', 'auth2')
		
		# Operation options
		self.update = self.config.get('operation', 'update')
		self.rollback = self.config.get('operation', 'rollback')

		# Use a VPN to upload
		self.via_vpn = self.config.get('vpn', 'via_vpn')			
		self.ip = self.config.get('vpn', 'ip')
		self.port = self.config.get('vpn', 'port')
		self.vpngate = self.config.get('vpn', 'vpngate')
		
		
	def show_info(self):
		"""Display the configuration info to debug."""
		# [gae] section		
		print("appid = %s" % self.appid)
		print("Goagent server source = %s" % self.goagent_server_src)
		print("Python interpretor: %s" % self.python)
		print("Location of GAE appcfg.py: %s" % self.gae_sdk_root)

		# [authentication] section
		print("with_email = %s" % self.with_email)
		print("Email box: %s" % self.email)		
		print("auth2: %s" % self.auth2)

		# [operation] section		
		print("update: %s" % self.update)
		print("rollback: %s" % self.rollback)		
		
		# [vpn] section
		print("via_vpn: %s" % self.via_vpn)		
		print("ip: %s" % self.ip)
		print("port: %s" % self.port)
		print("vpngate: %s" % self.vpngate)


	def validate(self):
		"""Check whether the Goagent server side source and the gae SDK installation directory exist.
		And validate the format of appids. Much of the code is based on Phus Lu's uploader.
		"""
		assert os.path.exists(self.goagent_server_src), u'Directory %s does *NOT* exists!' % self.goagent_server_src
		assert os.path.exists(self.gae_sdk_root), u'Directory %s does *NOT* exists!' % self.gae_sdk_root	
	
		if not re.match(r'[0-9a-zA-Z\-|]+', self.appid):
			println(u"错误的 appid 格式，请登录 http://appengine.google.com 查看您的 appid！\n \
				Wrong appid format, please log on to http://appengine.google.com to confirm your appid!")
			sys.exit(-1)
		
		if any(x in self.appid.lower() for x in ('ios', 'android', 'mobile')):
			println(u'appid 不能包含 ios/android/mobile 等字样！\n \
				Do not use the reserved key words ios/android/mobile!')
			sys.exit(-1)


if __name__ == '__main__':
	gdcp = GDeployerConfigParser()
	gdcp.show_info()
	gdcp.validate()
	#print("--- Work done!")
	
