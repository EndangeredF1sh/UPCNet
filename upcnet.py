import requests, urllib, os, base64, time, sys
from getpass import getpass


# 全局变量
filePath = os.path.split(os.path.realpath(__file__))[0] + '/config.ini'  # 加密后的账号密码储存在根目录下
argParsed = ""
trueText = ""
trueUrl = ""


def servicechoose(serv):  # 运营商选择
    if serv == '1': return "default"  # 校园网
    elif serv == '2': return "unicom"  # 联通
    elif serv == '3': return "cmcc"  # 移动
    elif serv == '4': return "ctcc"  # 电信
    return "local"  # 校园内网


def encode(string):  # 加密
    return base64.encodebytes(str.encode(string, 'utf-8'))


def decode(code):  # 解密
    return bytes.decode(base64.decodebytes(code), 'utf-8')


def autoexit(code):
    time.sleep(1)
    sys.exit(code)


def online():
    try:
        query = requests.get("http://www.lucien.ink/test", timeout=5)
        return query.text == 'Hello World!'
    except: return False


class NotRouterError(ValueError): pass


def login():  # 登录模块
    global argParsed, trueText, trueUrl
    address = "http://121.251.251.207"  # 默认尝试进行有线登录
    try:
        trueUrl = requests.post("http://121.251.251.217", allow_redirects=True).url
        trueText = requests.get("http://121.251.251.217", allow_redirects=True).text

        # if trueText.find("http://121.251.251.217") > 0 and trueUrl.find("http://www.upc.edu.cn") == 0:
        if trueText.find("http://121.251.251.217") > 0:
            raise NotRouterError()

    except requests.exceptions.ConnectionError:
        # macOS的登录界面会阻断网络连接
        print("Please check the network connection or close the login windows")
        autoexit(1)

    except NotRouterError:
        address = "http://121.251.251.217/"
        pIndex = requests.get(address, allow_redirects=True).text.find('wlanuserip')
        argParsed = urllib.parse.quote(trueText[pIndex:])

    else:
        argParsed = urllib.parse.quote(urllib.parse.urlparse(trueUrl).query)

    if argParsed.find('wlanuserip') == -1:
        if online():
            print("Already online")  # 已经登录
            autoexit(0)
        else:
            userIndex = urllib.parse.urlparse(trueUrl).query[10:]
            if address.find('217'):
                requests.post("http://121.251.251.217/eportal/InterFace.do?method=logout",
                              data={'userIndex': userIndex})
            else:
                requests.post("http://121.251.251.207/eportal/InterFace.do?method=logout",
                              data={'userIndex': userIndex})
            login()

    url = address + "/eportal/InterFace.do?method=login"

    str = decode(open(filePath, "rb").readline())  # 读取二进制文件并解密
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
    autoexit(0)


def upcnet():
    global argParsed, trueText, trueUrl
    argParsed = ""
    trueText = ""
    trueUrl = ""
    if not os.path.exists(filePath):
        # print(fontType.red + 'When using for the first time, please complete the imformation first' + fontType.red)
        # 把账号信息压进一个字符串后进行加密
        str_tmp = input('School number: ')
        # str_tmp = str_tmp + ' ' + input(fontType.green + 'Password(Invisible)' + fontType.tail + ': ')
        str_tmp = str_tmp + ' ' + getpass('Password: (Hidden)')
        str_tmp = str_tmp + ' ' + input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\n'
                                        'Communications number: ')
        file = open(filePath, 'wb')
        file.write(encode(str_tmp))  # 加密后的字符串写入二进制文件

    login()


def main():
    if len(sys.argv) > 1:
        if (len(sys.argv) > 2):
            print('Too many args')
            autoexit(1)

        if sys.argv[1] == 'reset':
            if os.path.exists(filePath):
                os.remove(filePath)
            print('Reset successful')
            autoexit(0)

        print('Wrong args')
        autoexit(1)

    else: upcnet()


if __name__ == '__main__':
    main()
