import requests
import urllib
from urllib.parse import urlparse
trueUrl = requests.post("http://121.251.251.207", allow_redirects=True).url
userIndex = urlparse(trueUrl).query[10:]
print("By LucienShui & EndangeredF1sh")
print("------------------------------")
requests.post("http://121.251.251.207/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})
print("退出成功！")
exit(0)
