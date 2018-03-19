import requests
import urllib
import getpass
from urllib.parse import urlparse
from config import username
from config import password
from config import serv


class NotRouterError(ValueError):
    pass

argParsed = ""
address = "http://121.251.251.207"
try:
    trueUrl = requests.post("http://121.251.251.217", allow_redirects=True).url
    trueText = requests.get("http://121.251.251.217", allow_redirects=True).text

    if trueText.find("http://121.251.251.217") > 0 and trueUrl.find("http://www.upc.edu.cn") == 0:
        raise NotRouterError()
except requests.exceptions.ConnectionError:
    print("网络连接故障,请检查网络连接或关闭系统弹出的认证窗口!")
    exit(-1)
except NotRouterError:
    address = "http://121.251.251.217/"
    pIndex = requests.get(address, allow_redirects=True).text.find('wlanuserip')
    argParsed = urllib.parse.quote(trueText[pIndex:])
    print("当前连接的是UPC热点")

else:
    argParsed = urllib.parse.quote(urlparse(trueUrl).query)

if argParsed.find('wlanuserip') == -1:
    print("当前状态为已登录")
    exit(0)

url = address+"/eportal/InterFace.do?method=login"
userName = username
passWord = password
service = serv
payload = {'userId': userName, 'password': passWord, 'service': service, 'queryString': argParsed, 'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
postMessage = requests.post(url, data=payload)
if postMessage.text.find("success") >= 0:
    print("登陆成功")
else:
    print("登陆失败")
    exit(0)