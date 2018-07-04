import base64
import time
import sys
import os
import requests


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


def getpath():
    return os.path.split(os.path.realpath(__file__))[0] + '\config.ini'  # 加密后的账号密码储存在根目录下


def online(): # （已弃用）测试当前是否有外网
    text = requests.get("https://api.zhihu.com/test", allow_redirects=True).text # 对知乎发请求，存储返回值
    return text.find('400') != -1
