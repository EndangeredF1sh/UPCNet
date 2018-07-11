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


def config_init():
    file_path = getpath()
    if not os.path.exists(file_path):
        str_tmp = input('School number: ')
        str_tmp = str_tmp + ' ' + getpass('Password: (Hidden)')
        str_tmp = str_tmp + ' ' + input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\nCommunications number: ')
        file = open(file_path, 'wb')
        file.write(encode(str_tmp))  # 加密后的字符串写入二进制文件


arg_parsed = text = address = ""  # 全局变量
cnt_try = 0  # 当前的尝试次数


def init_net():  # 登录模块
    global arg_parsed, text, cnt_try, address
    arg_parsed = text = ""

    try:
        text = requests.get("http://captive.lucien.ink", allow_redirects=True).text

    except:
        cnt_try = cnt_try + 1
        if cnt_try >= 5:
            print("Please check the network connection or close the login windows")
            return False
        time.sleep(1)
        return init_net()

    if ~text.find("Hello"):
        print("Currently online")
        return False

    else:
        if ~text.find("121.251.251.217"):
            address = "http://121.251.251.217"
            arg_parsed = urllib.parse.quote(text[text.find('wlanuserip'):])

        else:
            address = "http://121.251.251.207"
            arg_parsed = urllib.parse.quote(urllib.parse.urlparse(requests.post("http://captive.lucien.ink", allow_redirects=True).url).query)

    return True


def login():
    if init_net():
        global arg_parsed, address
        if not ~arg_parsed.find('wlanuserip'):
            logout()
            global cnt_try
            cnt_try = cnt_try + 1
            if cnt_try >= 5:
                print("Please check the network connection or close the login windows")
                return False
            time.sleep(1)
            return login()

        buf = decode(open(getpath(), "rb").readline())  # 读取二进制文件并解密

        payload = {'userId': buf.split(' ')[0], 'password': buf.split(' ')[1],
                   'service': service_choose(buf.split(' ')[2]), 'queryString': arg_parsed,
                   'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
        post_message = requests.post(address + "/eportal/InterFace.do?method=login", data=payload)

        if post_message.text.find("success") >= 0:
            print("Login success")  # 登录成功
            return True

        else:
            print("Something wrong")  # 登录失败
            return False

    return False


def logout():
    try:
        requests.post("http://121.251.251.207/eportal/InterFace.do?method=logout")
        requests.post("http://121.251.251.217/eportal/InterFace.do?method=logout")

    except:
        print("Logout failed")

    else:
        print("Logout success")


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
        login()

    autoexit()
