# -*- encoding: utf8-*-
import requests
import urllib
import getpass
from urllib.parse import urlparse


class NotRouterError(ValueError):
    pass


def servicechoose(serv):
    try:
        if serv == '1':
            return "default"
        elif serv == '2':
            return "unicom"
        elif serv == '3':
            return "cmcc"
        elif serv == '4':
            return "ctcc"
        elif serv == '5':
            return "local"
        else:
            print("Input failed!")
    except Exception:
        print("输入类型有误！请重新运行程序")
        exit(1)


argParsed = ""
address = "http://121.251.251.207"
try:
    trueUrl = requests.post("http://121.251.251.217", allow_redirects=True).url
    trueText = requests.get("http://121.251.251.217", allow_redirects=True).text
    # print(trueUrl)
    # print(trueText)
    if trueText.find("http://121.251.251.217") > 0 and trueUrl.find("http://www.upc.edu.cn") == 0:
        raise NotRouterError()
except requests.exceptions.ConnectionError:
    print("网络连接故障,请检查你的网络连接或关闭系统弹出认证窗口！")
    exit(-1)
except NotRouterError:
    address = "http://121.251.251.217/"
    pIndex = requests.get(address, allow_redirects=True).text.find('wlanuserip')
    argParsed = urllib.parse.quote(trueText[pIndex:])
    print("你连接的是UPC热点!")

else:
    argParsed = urllib.parse.quote(urlparse(trueUrl).query)

if argParsed.find('wlanuserip') == -1:
    print("你已经登录！")
    userIndex = urlparse(trueUrl).query[10:]
    if input("输入0退出登录，其他输入则忽略: ") == '0':
        requests.post("http://121.251.251.217/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
        requests.post("http://121.251.251.207/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
        print("退出成功！")
        exit(0)
    else:
        print("保持登录！")
        exit(0)
url = address+"/eportal/InterFace.do?method=login"
userName = input("输入你的数字石大账户：")
passWord = getpass.getpass("输入你的数字石大密码：")
service = servicechoose(input("输入运营商(1为校园网，2为联通，3为移动，4为电信,5为校园内网):"))
payload = {'userId': userName, 'password':passWord, 'service': service, 'queryString': argParsed,'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
postMessage = requests.post(url,data=payload)
# print(postMessage.text)
if postMessage.text.find("success") >= 0:
    print("登陆成功")
else:
    print("登陆失败")
    exit(0)

