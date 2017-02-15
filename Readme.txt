1. gdeployer是什么？
GAE/Goagent服务端批量部署工具。


2. 如何不使用gdeployer？
如何您使用Goagent创立者Phus Lu的uploader.bat或uploader.py工具能成功上载Goagent服务端，不必使用此工具，因为它配置复杂。否则可尝试。


3. 如何使用gdeployer？

3.1 必须先安装Google App Engine SDK for Python。官方地址地址 https://cloud.google.com/appengine/downloads 被墙，请翻墙下载或搜索墙内的下载. 1.8及以上的版本都没问题。

3.2 运行前，请仔细阅读和修改部署配置文件 gdeploy.ini，以适应您的具体情况。

3.3 本工具需使用Python环境运行，您可安装完整的2.7及以上版本的Python (http://www.python.org)，也可使用Goagent自带的Python解释器python27.exe。

3.4 确保部署配置文件 gdeploy.ini 无误后，Windows/Unix/Linux/Mac 用户, 在命令行使用 python gdeployer.py 或 python27 gdployer.py来运行；Windows用户还可双击 gdeployer.bat 来运行。

3.5 当前版本仅支持两步验证。若未开启，在第一次执行时会自动引导您设置（需借助VPN），以后再不需要设置，除非重新了系统或换了PC。


4. 反馈：请发到 https://code.google.com/p/gdeployer/issues/list 。


----------------------------------------------------------
1. What is gdeployer?
A batch-deploying utility to deploy GAE/Goagent server.


2. How NOT to use it?
If you can use Goagent creator Phus Lu's uploader.bat or uploader.py to deploy the server side successfully, do not use this tool as it's complicated to configure. Otherwise, give it a try.


3. How  to use it?

3.1 Google App Engine SDK for Python has to be installed. The official website  https://cloud.google.com/appengine/downloads has been blocked within mainland China. Please search for an available one or circumvent the GFW to download it. Version 1.8 and above will do.

3.2 Please read and modify the deploying configuration file gdeploy.ini to meet your demands carefully.

3.3 Python runtime environment is needed to run this tool. Either a fully Python environment (http://www.python.org) or python27.exe bundled with Goagent will do.

3.4 Make sure that gdeploy.ini is correct in your specific conditions. On Windows/Unix/Linux/Mac, run from the command line: python gedeployer.py or python27 gdployer.py. The other alternative for Windows users is to double-click deployer.bat.

3.5 Only 2-step authentication is supported now. If you haven't enabled it, you'll be guided to enable it the first time gdeployer runs. This has to be done with a VPN as google.com has been blocked within mainland China.  Once authenticated, no more authentication is needed when uploading thereafter
;; unless your OS is reinstalled or you start using a new PC.


4. Please send your feedback to website https://code.google.com/p/gdeployer/issues/list   .


5. Change History

Version		Description
20141001b The batch deploying functionality implemented fully with all the options supported. 