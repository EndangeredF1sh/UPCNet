import requests
import urllib
import os
import time
import base64
import sys
def service_choose(serv):  # 运营商选择
    if serv == '1': return "default"  # 校园网
    elif serv == '2': return "unicom"  # 联通
    elif serv == '3': return "cmcc"  # 移动
    elif serv == '4': return "ctcc"  # 电信
    return "local"  # 校园内网

def decode(code):  # 解密
    return bytes.decode(base64.decodebytes(code), 'utf-8')

def autoexit():
    time.sleep(1)
    sys.exit(0)

class NotRouterError(ValueError):
    pass

def login():  # 登录模块
    argParsed = ""
    try:
        trueUrl = requests.post("http://121.251.251.207", allow_redirects=True).url

    except requests.exceptions.ConnectionError:
        # macOS的登录界面会阻断网络连接
        print("Please check the network connection or close the login windows")
        autoexit()

    else:
        argParsed = urllib.parse.quote(urllib.parse.urlparse(trueUrl).query)

    if argParsed.find('wlanuserip') == -1:
        print("Already online")  # 已经登录
        autoexit()

    url = "http://121.251.251.207/eportal/InterFace.do?method=login"

    path = os.path.split(os.path.realpath(__file__))[0]
    if (os.name == 'nt'):
        path = path + "\\config.ini"
    else:
        path = path + "/config.ini"

    str = decode(open(path, "rb").readline())  # 读取二进制文件并解密
    userName = str.split(' ')[0]
    passWord = str.split(' ')[1]
    service = service_choose(str.split(' ')[2])

    payload = {'userId': userName, 'password': passWord, 'service': service, 'queryString': argParsed,
               'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
    postMessage = requests.post(url, data=payload)

    if postMessage.text.find("success") >= 0: print("Login success")  # 登录成功
    else: print("Something wrong")  # 登录失败
    autoexit()

login()
