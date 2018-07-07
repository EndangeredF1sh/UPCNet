import requests
import urllib
import os
import time
import base64
import sys
from getpass import getpass


def service_choose(serv):  # 运营商选择
    if serv == '1':
        return "default"  # 校园网
    elif serv == '2':
        return "unicom"  # 联通
    elif serv == '3':
        return "cmcc"  # 移动
    elif serv == '4':
        return "ctcc"  # 电信
    return "local"  # 校园内网


def encode(string):  # 加密
    return base64.encodebytes(str.encode(string, 'utf-8'))


def decode(code):  # 解密
    return bytes.decode(base64.decodebytes(code), 'utf-8')


def getpath():  # 返回账号密码的存储路径
    path = os.path.split(os.path.realpath(__file__))[0]  # 脚本根目录
    if os.name == "nt":  # Windows
        return path + "\\config.ini"  
    else:  # Linux
        return path + "/config.ini"


def config_init():
    file_path = getpath()
    if not os.path.exists(file_path):
        str_tmp = input('School number: ')
        str_tmp = str_tmp + ' ' + getpass('Password: (Hidden)')
        str_tmp = str_tmp + ' ' + input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\nCommunications number: ')
        file = open(file_path, 'wb')
        file.write(encode(str_tmp))  # 加密后的字符串写入二进制文件


def autoexit():
    time.sleep(1)
    sys.exit(0)


class NotRouterError(ValueError):
    pass


def login():  # 登录模块
    argParsed = ""
    try:
        trueUrl = requests.post("http://www.baidu.com", allow_redirects=True).url

    except requests.exceptions.ConnectionError:
        print("Please check the network connection or close the login windows")
        return False

    else:
        argParsed = urllib.parse.quote(urllib.parse.urlparse(trueUrl).query)

    if argParsed.find('wlanuserip') == -1:
        print("Already online")  # 已经登录
        return True

    url = "http://121.251.251.207/eportal/InterFace.do?method=login"

    str = decode(open(getpath(), "rb").readline())  # 读取二进制文件并解密
    userName = str.split(' ')[0]
    passWord = str.split(' ')[1]
    service = service_choose(str.split(' ')[2])

    payload = {'userId': userName, 'password': passWord, 'service': service, 'queryString': argParsed,
               'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
    postMessage = requests.post(url, data=payload)

    if postMessage.text.find("success") >= 0:
        print("Login success")  # 登录成功
        return True
    else:
        print("Something wrong")  # 登录失败
        return False


if __name__ == "__main__":
    config_init()
    login()
    autoexit()
