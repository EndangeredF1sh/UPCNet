#!/usr/bin/python3
#!coding=utf-8
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


def autoexit(): # 延时一秒后结束程序
    time.sleep(1)
    sys.exit()


def getpath(): # 返回账号密码的存储路径
    if os.name == "nt":
        path = os.environ['SYSTEMROOT'][:3] + "UPCNet"
        if not os.path.exists(path):
            os.makedirs(path)
        return path + "\\config.ini" # Windows返回C盘

    else:
        path = os.path.split(os.path.realpath(__file__))[0]
        return path + "/config.ini" # Linux返回脚本根目录


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

