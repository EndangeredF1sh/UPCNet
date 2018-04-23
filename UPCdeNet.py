import requests
import urllib
import time

def autoexit():
    print("3 seconds later exit")
    time.sleep(3)
    exit(0)

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
    print("Please check the network connection or close the login windows")  # macOS的登录界面会阻断网络连接
    autoexit()

except NotRouterError:
    address = "http://121.251.251.217/"
    pIndex = requests.get(address, allow_redirects=True).text.find('wlanuserip')
    argParsed = urllib.parse.quote(trueText[pIndex:])

else:
    argParsed = urllib.parse.quote(urllib.parse.urlparse(trueUrl).query)

if argParsed.find('wlanuserip') == -1:
    userIndex = urllib.parse.urlparse(trueUrl).query[10:]
    requests.post("http://121.251.251.217/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
    requests.post("http://121.251.251.207/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
    print("Logout success") # 退出成功
else:
    print('Something wrong')

autoexit()
