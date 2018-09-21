#!/usr/bin/python3
#!coding=utf-8
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
    return "%s%sconfig.ini" % (path, os.path.sep)


def config_init():
    file_path = getpath()
    if not os.path.exists(file_path):
        str_tmp = input('School number: ')
        str_tmp = str_tmp + ' ' + getpass('Password: (Hidden)')
        str_tmp = str_tmp + ' ' + input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\nCommunications number: ')
        file = open(file_path, 'wb')
        file.write(encode(str_tmp))  # 加密后的字符串写入二进制文件


def online():
    try:
        url = requests.get("http://captive.lucien.ink", allow_redirects=True, timeout=3).url
    except:
        return False  # 超时，当前无外网
    if ~url.find("https://www.lucien.ink"):
        return True  # 当前有外网
    return False


arg_parsed = url = address = ""  # 全局变量
cnt_try = 0  # 当前的尝试次数


def init_net():  # 登录模块
    global arg_parsed, url, cnt_try, address
    arg_parsed = url = ""
    address = "http://121.251.251.217"

    try:
        url = requests.get(address, allow_redirects=True, timeout=3).url

    except:
        cnt_try = cnt_try + 1
        if cnt_try >= 5:
            print("Please check the network connection or close the login windows")
            return False
        time.sleep(1)
        return init_net()

    else:
        if ~url.find("121.251.251.207"):
            address = "http://121.251.251.207"
            buf = requests.post(address, allow_redirects=True).url
            arg_parsed = urllib.parse.quote(urllib.parse.urlparse(buf).query)

        else:
            address = "http://121.251.251.217"
            buf = requests.post(address, allow_redirects=True).text
            arg_parsed = urllib.parse.quote(buf[buf.find('wlanuserip'):])

    return True


def login():
    if online():
        print("Currently online")
        return False
    if init_net():
        global arg_parsed, address, url
        if ~url.find('success') or ~url.find("www.upc.edu.cn"):
            logout()
            global cnt_try
            cnt_try = cnt_try + 1
            if cnt_try >= 5:
                print("Please check the network connection or close the login windows")
                return False
            time.sleep(1)
            return login()

        buf = decode(open(getpath(), "rb").readline())  # 读取二进制文件并解密

        payload = {'userId': buf.split(' ')[0],
                   'password': buf.split(' ')[1],
                   'service': service_choose(buf.split(' ')[2]),
                   'queryString': arg_parsed,
                   'operatorPwd': '',
                   'operatorUserId': '',
                   'vaildcode': '',
                   'passwordEncrypt': 'false'}
        post_message = requests.post(address + "/eportal/InterFace.do?method=login", data=payload)

        if post_message.text.find("success") >= 0 and online():
            print("Login success")  # 登录成功
            return True

        else:
            print("Something wrong")  # 登录失败
            return False

    return False


def out(address):
    try:
        url = requests.get(address, allow_redirects=True, timeout=3).url
        if ~url.find("userIndex="):
            userIndex = url[url.find("userIndex=") + 10:]
            requests.post(address + "/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
    except:
        return


def logout():
    try:
        out("http://121.251.251.217")
        out("http://121.251.251.207")

    except:
        print("Logout failed")

    else:
        if online():
            print("Logout failed")
        else:
            print("Logout success")


if __name__ == '__main__':
    # logout()
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
        login()

    autoexit()
