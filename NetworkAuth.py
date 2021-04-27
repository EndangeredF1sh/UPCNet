# -*- coding:utf-8 -*-
import requests
import urllib
from urllib.parse import urlparse
from config import username
from config import password
from config import serv
url = ""
argParsed = ""
address = "http://121.251.251.217"
magic_word = "/&userlocation=ethtrunk/62:3501.0"
lan_special_domain = "http://lan.upc.edu.cn"
login_parameter = "/eportal/InterFace.do?method=login"
try:
    trueText = requests.get(address + magic_word, allow_redirects=True).text
    trueUrl = requests.post(address + magic_word, allow_redirects=True).url
    url = lan_special_domain+login_parameter
    if trueText.find("Error report") > -1:
        trueUrl = requests.post("http://121.251.251.207" + magic_word, allow_redirects=True).url  # 特殊处理
        url = address + login_parameter
    argParsed = urllib.parse.quote(urlparse(trueUrl).query)
    if argParsed.find('wlanuserip') == -1:
        print("你已经登录！")
        exit(0)
except requests.exceptions.ConnectionError:
    print("网络连接故障,请检查你的网络连接或关闭系统弹出认证窗口！")
    exit(-1)

payload = {'userId': username, 'password': password, 'service': serv, 'queryString': argParsed, 'operatorPwd': '', 'operatorUserId': '', 'validcode': '', 'passwordEncrypt': 'false'}
postMessage = requests.post(url, data=payload)
if postMessage.text.find("success") >= 0:
    print("登陆成功")
else:
    print("登陆失败")
    exit(0)

