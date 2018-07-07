#!/usr/bin/python3
# !coding=utf-8
import urllib
import base64
import time
import os
import requests
import sys
from getpass import getpass


def service_choose(service):  # 运营商选择
    if service == '1':
        return "default"  # 校园网
    elif service == '2':
        return "unicom"  # 联通
    elif service == '3':
        return "cmcc"  # 移动
    elif service == '4':
        return "ctcc"  # 电信
    return "local"  # 校园内网


def encode(string):  # 加密
    return base64.encodebytes(str.encode(string, 'utf-8'))


def decode(code):  # 解密
    return bytes.decode(base64.decodebytes(code), 'utf-8')


def autoexit():  # 延时一秒后结束程序
    time.sleep(1)
    sys.exit()


def getpath():  # 返回账号密码的存储路径
    path = os.path.split(os.path.realpath(__file__))[0]  # 脚本根目录
    if os.name == "nt":
        return path + "\\config.ini"  # Windows
    else:
        return path + "/config.ini"  # Linux


def online():
    try:
        text = requests.get("http://acm.upc.edu.cn/404.", allow_redirects=True, timeout=5).text
    except:
        return False
    return text.find('404') != -1


def config_init():
    file_path = getpath()
    if not os.path.exists(file_path):
        str_tmp = input('School number: ')
        str_tmp = str_tmp + ' ' + getpass('Password: (Hidden)')
        str_tmp = str_tmp + ' ' + input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\nCommunications number: ')
        file = open(file_path, 'wb')
        file.write(encode(str_tmp))  # 加密后的字符串写入二进制文件


argParsed = trueText = trueUrl = address = ""  # 全局变量
cntTry = 0  # 当前的尝试次数


class NotRouterError(ValueError):
    pass


def init_net():  # 登录模块
    global argParsed, trueText, trueUrl, cntTry, address
    argParsed = trueText = trueUrl = ""
    address = "http://121.251.251.207"  # 默认尝试进行有线登录

    try:
        trueUrl = requests.post("http://121.251.251.217", allow_redirects=True).url
        trueText = requests.get("http://121.251.251.217", allow_redirects=True).text

        # if trueText.find("http://121.251.251.217") > 0 and trueUrl.find("http://www.upc.edu.cn") == 0:
        if trueText.find("http://121.251.251.217") > 0:
            raise NotRouterError()

    except requests.exceptions.ConnectionError:
        print("Please check the network connection or close the login windows")
        return False  # macOS的登录界面会阻断网络连接

    except NotRouterError:
        address = "http://121.251.251.217/"
        pIndex = trueText.find('wlanuserip')
        # pIndex = requests.get(address, allow_rdirects=True).text.find('wlanuserip')
        argParsed = urllib.parse.quote(trueText[pIndex:])

    except requests.exceptions.ChunkedEncodingError:
        cntTry = cntTry + 1
        if cntTry >= 5:
            print("Please check the network connection or close the login windows")
            return False
        return init_net()

    else:
        argParsed = urllib.parse.quote(urllib.parse.urlparse(trueUrl).query)

    return True


def login():
    if init_net():
        global argParsed, address
        if argParsed.find('wlanuserip') == -1:
            logout()
            time.sleep(2)
            return login()

        url = address + "/eportal/InterFace.do?method=login"

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

    return False


def logout():
    global trueUrl, address
    userIndex = urllib.parse.urlparse(trueUrl).query[10:]
    if address.find('217'):
        requests.post("http://121.251.251.217/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
    else:
        requests.post("http://121.251.251.207/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
    print('Logout success')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print('Too many args')

        else:
            argv = sys.argv[1]
            if argv == 'reset':
                file_path = getpath()
                if os.path.exists(file_path):
                    os.remove(file_path)
                print('Reset successful')

            elif argv == 'logout':
                logout()

            else:
                print('Wrong args')

    else:
        config_init()

        if online():
            print("Already online")  # 已经登录

        else:
            login()
