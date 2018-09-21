# 中国石油大学（华东）校园网络认证脚本

### 依赖
本脚本采用Python3编写，依赖于
````
Requests
urllib/urllib.parse
````
快速安装依赖
```
pip install -r requirements.txt
```

### 使用方法
在config.py文件下输入学号、密码和运营商编号，然后运行
```
python3 NetworkAuth.py
```

运营商对应编号：

```
default -> 校园网
unicom -> 联通
cmcc -> 移动
ctcc -> 电信
local -> 校园内网
```
可自动判别登录情况，引导用户交互。


### 目前支持的网络类型：
````
有线网络（认证IP地址:121.251.251.207)

无线网络(SSID: UPC, 认证IP地址:121.251.251.217)

802.1X网络无需使用本脚本

````

### 测试环境
```
macOS 10.13.1
Windows 10 (Build 17134)
```

### 版权信息
````
Author：EndangeredFish

Email: zwy346545141@gmail.com

First Commit Date:  Monday,13 Nov 2017 

LICENSE: AGPLv3
````
