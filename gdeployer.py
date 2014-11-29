#!/usr/bin/env python
# coding:utf-8
# Based on Phus Lu's Goagent uploader.py.
# Author:
#      Guanglin Du <guanglin.du@gmail.com>

"""
gdeployer.py: Batch-deploy Goagent server side on to GAE, the main program.

Much of the code is based on Phus Lu's original uploader.py bundled with Goagent (https://code.google.com/p/goagent).
Many thanks to Phus Lu and all Goagent contributors who opened a large window toward the outside world.

Howtos:
1. Please edit the configuration file gdeployer.ini carefully before running it.
2. On any platform (Windows/Unix/Linux/Mac OS) with Python installed, run from the command line: python gdeployer.py.
3. On Windows, a started is created, gdeployer.bat, to support the double-click running. 
"""

import sys
import os
import re
import platform
import gdeployer_config_parser

# Versions based on date
__version__ = '20141001b'

# A temporary batch (Windows) or shell (Unix/Linux) file to run the task
__TBAT__ = 't.bat'
	
# A global variable to load file gdeployer.ini, the configuration info.
gdcp = gdeployer_config_parser.GDeployerConfigParser()


# The same method as the one in uploader.py
def println(s, file=sys.stderr):
	assert type(s) is type(u'')
	file.write(s.encode(sys.getfilesystemencoding(), 'replace') + os.linesep)


def update_app_yaml(dirname, appid):
	"""Update the app.yaml file for each appid and upload the gae dir. Much is the same as the one in uploader.py.
	
	Keyword arguments:
	dirname -- the directory (path) of Goagent server source, usually, ...\server\gae\
	appid -- the appid to be uploaded/updated/rolled-back
	"""
	assert isinstance(dirname, basestring) and isinstance(appid, basestring)
	
	# From goagent 3.2.2 on, file app.template.yaml replaced file app.yaml
	src = os.path.join(dirname, "app.template.yaml") # source	
	filename = os.path.join(dirname, "app.yaml") # destination
	if not os.path.isfile(filename):
		assert os.path.isfile(src), u'%s not exists!' % src
		shutil.copy2(src, filename)
	#assert os.path.isfile(filename), u'%s not exists!' % filename
	
	with open(filename, 'rb') as fp:
		yaml = fp.read()
	
	# Substitute the old appid with the current one
	yaml = re.sub(r'application:\s*\S+', 'application: ' + appid, yaml)
	with open(filename, 'wb') as fp:
		fp.write(yaml)

	
def run_on_Windows():
	"""Run the shell script to upload/update/rollback the app on Windows."""
	# cd to the folder where appcfg.py resides to execute to avoid the module dependency error!!!
	#os.chdir(gdcp.appcfg)
	# Lop for the appids to do the batch action
	for appid in gdcp.appid.split('|'):
		update_app_yaml(gdcp.goagent_server_src, appid)
		print("\ngdeployer: %s is to be uploaded/rolled-back from Windows ..." % appid)
		os.system(__TBAT__)


def run_on_Linux():
	"""Run the shell script to upload/update/rollback the app on Unix/Linux/Mac OS."""
	# cd to the folder where appcfg.py resides to execute to avoid the module dependency error!!!
	#os.chdir(gdcp.appcfg)
	# Loop for the appids to do the batch action
	for appid in gdcp.appid.split('|'):
		update_app_yaml(gdcp.goagent_server_src, appid)
		print("\ngdeployer: %s is to be uploaded/rolled-back from Unix/Linux/Mac OS ..." % appid)
		# Use "sh t.bat" to execute the script 
		os.system("sh " + __TBAT__)

		
def set_proxy_on_Windows(cmd_list):
	"""Create the cmd to set the https_proxy environment variable on Windows.
	On Windows, we use the command SET key=value to set an evironment varialbe, e.g.,
	setting HTTPS_PROXY environment variable pointing to Freegate
	SET HTTPS_PROXY=https://127.0.0.1:8580
	
	Keyword arguments:
	cmd_list -- the command list, a Python list, with its 1st element to set https_proxy or not.	 	
	"""
	if(cmd_list[0] == "novpn"):
		cmd_list[0] = "@REM No VPN is used is used to upload.\n"
	elif(cmd_list[0] == "vpngate"):
		cmd_list[0] = "@REM vpngate is used to upload.\n"
	else:
		cmd_list[0] = "SET " + cmd_list[0]
	
	return cmd_list

	
def set_proxy_on_Linux(cmd_list):
	"""Create and run a shell script on Unix/Linux/Mac OS.
	 On Unix/Linux/Mac OS, we use the command export key=value to set an evironment varialbe, e.g.
	set HTTPS_PROXY environment variable pointing to Freegate
	# export HTTPS_PROXY=https://127.0.0.1:8580
	 
	Keyword arguments:
	cmd_list -- the command list, a Python list, with its 1st element to set https_proxy or not.	 	
	"""
	if(cmd_list[0] == "novpn"):
		cmd_list[0] = "# No VPN is used to upload.\n"
	elif(cmd_list[0] == "vpngate"):
		cmd_list[0] = "# vpngate is used to upload.\n"
	else:
		cmd_list[0] = "export " + cmd_list[0]

	return cmd_list


def create_shell_script(cmd_list):
	"""Create the shell script, the t.bat file.
	A batch file on Windows, and a shell file on Unix/Linux/Mac OS.
	Attention: Here is a pitfall to access the environment variable set by the shell script.
		The environment variable set by a shell script is not necessarily accessed by another script
		unless that variable is global. Hence, here we have to write the https_proxy variable in the
		same shell file as the command "python appcfg.py ...".
	
	Keyword arguments:
	cmd_list -- the command list, a Python list, with its element 0 and to be further appended
		with the python appcfg.py ... command.
	"""
	# Use the 2-step authentication to upload by command like the following, e.g, on Windows,
	# python  ...\path\to\appcfg.py --oauth2 --email=xxx@gmail.com update ...\path\to\goagent-3.2.0\server\gae	
	# Determine do with or without an authentication. 2-step authentication recommended
	#auth = "" # without an authentication
	auth = " --oauth2 " # Only 2-step authentication supported now
	# auth_flag = gdcp.auth2.lower()
	# if(auth_flag == "yes" or auth_flag == "y"):
		# auth = " --oauth2 "
		
	# With or without email
	email_arg = ""
	email_flag = gdcp.with_email.lower()
	if(email_flag == "yes" or email_flag == "y"):
		email_arg = " --email=" + gdcp.email
	
	# Rollback first if the rollback flag is yes
	# Determine whether or not the path separator is already appenped by the user in gdeployer.ini,
	# and Create the python appcfg.py rollback ... /path/to/server/src command line.
	rollback_flag = gdcp.rollback.lower()
	if(rollback_flag == "yes" or rollback_flag == "y"):
		cmd_list.append(gdcp.python + " " \
			+ append_path_separator(gdcp.gae_sdk_root) + "appcfg.py " \
			+ auth \
			+ email_arg  \
			+ " rollback " \
			+ gdcp.goagent_server_src +"\n")
		
	# Update
	# Determine whether or not the path separator is already appenped by the user in gdeployer.ini,
	# and Create the python appcfg.py update ... /path/to/server/src command line.
	update_flag = gdcp.update.lower()
	if(update_flag == "yes" or update_flag == "y"):
		cmd_list.append(gdcp.python + " " \
			+ append_path_separator(gdcp.gae_sdk_root) + "appcfg.py " \
			+ auth \
			+ email_arg  \
			+ " update " \
			+ gdcp.goagent_server_src +"\n")
	#print("cmd: %s" % cmd_list)

	# Create the shell script (the same file name on both Windows and Unix/Linux/Mac OS)
	f = open(__TBAT__, "w")
	for cmd in cmd_list:
		f.write(cmd)
	f.close()	


def append_path_separator(dir): 
	"""Make sure that the path ends with a path separator
	
	Keyword arguments:
	dir -- the passed path(directory) to be examined
	"""
	path_tail = os.path.sep # or os.sep
	if(not dir.endswith(path_tail)):
		dir = dir + path_tail
	return dir


def main():
	"""Update the app.yaml, create the script file to set https_proxy, run the "python appconf.py ..." command repeatedly."""
	# Validate the Goagent server source and gae SDK installation paths the appids.
	gdcp.validate()
	
	# Create the shell script first in 4 steps.
	# Command list used to output to a temporary bat file to overcome
	# that script cannot modify the parent cmd window's evironment variables.
	cmd_list = []
	
	# Step 1: Determines whether the https_proxy environment variable should be set
	# Upload via a VPN
	vpn_flag = gdcp.via_vpn.lower()
	if(vpn_flag == "yes" or vpn_flag == "y"):
		# If vpngate is in use, no proxy needed
		if(gdcp.vpngate == "yes" or gdcp.vpngate == "y"):
			cmd_list.append("vpngate")
		else:
			cmd_list.append("HTTPS_PROXY=https://" + gdcp.ip + ':' + gdcp.port + "\n")
	# If VPN is disabled, no proxy needed(the same effect as the case of using vpngate which is global).
	else:
		cmd_list.append("novpn")
	
	# Setp 2: Create the cmd to SET(Windows)/export(Unix/Linux/Mac OS) the https_proxy.
	# Step 3: Create the cmd "python appcfg.py ..." to upload/update/rollback the app.
	# Step 4: Run the script.
	# Do the magic by creating a temporary script file on Windows/Unix/Linux/Mac OS
	osid = platform.system().lower()
	# Windows...	
	if osid == "windows":
		cmd_list = set_proxy_on_Windows(cmd_list)
		create_shell_script(cmd_list)
		run_on_Windows()
	# Unix/Linux/Mac OS
	elif osid == "linux" or osid == "darwin":
		cmd_list = set_proxy_on_Linux(cmd_list)
		create_shell_script(cmd_list)
		run_on_Linux()
    # Unsupported OS
	else:
		print("Unknown OS id: %s. gdeployer cannot run. Please feedback to the developer." % osid) 
			

if __name__ == '__main__':
	println(u'''\
===============================================================================
批量GoAgent服务端部署工具：
1. 基于Google App Engine SDK for Python并使用了Phus Lu的uploader.py中的部分代码；
2. 运行前请细心编辑配置文件gedeployer.ini；
3. Windows/Unix/Linux/Mac 用户, 使用 python gdeployer.py 来运行；
4. Windows用户可使用gdeployer.bat来运行
    ------------------------------
 Goagent server batch-deploying utility:
1. Based on Google App Engine SDK for Python and copied much of Phus Lu's original uploader.py;
2. Edit the configuration file gdeployer.ini carefully before running;
3. On Windows/Unix/Linux/Mac, run from the command line: python gedeployer.py;
4. The other alternative for Windows users is to double-click deployer.bat.
==============================================================================='''.strip())
	main()
	println(os.linesep + u'上传成功后，请不要忘记编辑proxy.ini或proxy.user.ini 把您的appid填进去。按回车键退出。 \
After successful deployment, add the appids to Goagent configuration file proxy.ini or proxy.user.ini. \
Press Enter/Return key to exit. Thanks.')
	raw_input()
