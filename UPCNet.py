import requests
import urllib
import os
from urllib.parse import urlparse
import base64

def servicechoose(serv): # 运营商选择
    if serv == '1': return "default" # 校园网
    elif serv == '2': return "unicom" # 联通
    elif serv == '3': return "cmcc" # 移动
    elif serv == '4': return "ctcc" # 电信
    return "local" # 校园内网

def encode(string): # 加密
    return base64.encodebytes(str.encode(string, 'utf-8'))

def decode(code): # 解密
    return bytes.decode(base64.decodebytes(code), 'utf-8')

class NotRouterError(ValueError):
    pass

filename = './config.ini' # 加密后的账号密码储存在根目录下

def login(): # 登录模块
    argParsed = ""
    address = "http://121.251.251.207" # 默认尝试进行有线登录
    try:
        trueUrl = requests.post("http://121.251.251.217", allow_redirects=True).url
        trueText = requests.get("http://121.251.251.217", allow_redirects=True).text

        if trueText.find("http://121.251.251.217") > 0 and trueUrl.find("http://www.upc.edu.cn") == 0:
            raise NotRouterError()

    except requests.exceptions.ConnectionError:
        print("Please check the network connection or close the login windows")  # macOS的登录界面会阻断网络连接
        exit(-1)

    except NotRouterError:
        address = "http://121.251.251.217/"
        pIndex = requests.get(address, allow_redirects=True).text.find('wlanuserip')
        argParsed = urllib.parse.quote(trueText[pIndex:])

    else:
        argParsed = urllib.parse.quote(urlparse(trueUrl).query)

    if argParsed.find('wlanuserip') == -1:
        print("Already online")  # 已经登录
        exit(0)

    url = address + "/eportal/InterFace.do?method=login"

    str = decode(open(filename, "rb").readline()) # 读取二进制文件并解密
    userName = str.split(' ')[0]
    passWord = str.split(' ')[1]
    service = servicechoose(str.split(' ')[2])

    payload = {'userId': userName, 'password': passWord, 'service': service, 'queryString': argParsed,
               'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
    postMessage = requests.post(url, data=payload)
    if postMessage.text.find("success") >= 0:
        print("Login success")  # 登录成功
    else:
        print("Something wrong")  # 登录失败
        exit(0)

if os.path.exists(filename):
    login()
else:
    print('No user data, please input your account imformation.')
    with open(filename, 'wb') as file: # 二进制文件写入
        # 把账号信息压进一个字符串后进行加密
        str_tmp = input('School number:\n')
        str_tmp = str_tmp + ' ' + input('Password:\n')
        str_tmp = str_tmp + ' ' + input('Communications:\n1.default 2.unicom 3.cmcc 4.ctcc 5.local\n')
        code = encode(str_tmp) # 加密
        file.write(code) # 写文件
    login()

