import requests
import urllib
import time
from urllib.parse import urlparse
def servicechoose(serv):
    if serv == '1': return "default"
    elif serv == '2': return "unicom"
    elif serv == '3': return "cmcc"
    elif serv == '4': return "ctcc"
    return "local"
trueUrl = requests.post("http://121.251.251.207", allow_redirects=True).url
argParsed = urllib.parse.quote(urlparse(trueUrl).query)
if argParsed.find('wlanuserip') == -1: 
	print("您已登录")
	time.sleep(1)
	exit(0)
str = open("./in.txt").readline()
url = "http://121.251.251.207/eportal/InterFace.do?method=login"
payload = {'userId': str.split(' ')[0], 'password': str.split(' ')[1], 'service': servicechoose(str.split(' ')[2]), 'queryString': argParsed,'operatorPwd': '', 'operatorUserId': '', 'vaildcode': ''}
postMessage = requests.post(url,data = payload)
if postMessage.text.find("success") >= 0: print("登陆成功")
else: print("登陆失败")
time.sleep(1)
exit(0)
