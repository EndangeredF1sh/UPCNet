#!coding=utf-8
import urllib
from tools import *
argParsed = trueText = trueUrl = address = "" # 全局变量
cntTry = 0 # 当前的尝试次数


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
        return False # macOS的登录界面会阻断网络连接

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

        payload = {'userId': userName, 'password': passWord, 'service': service, 'queryString': argParsed, 'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
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

