# 中国石油大学（华东）校园网络认证脚本

### 依赖
本脚本采用Python3编写，依赖于
````
Requests
urllib/urllib.parse
getpass
````

### 使用方法
输入数字石大用户名和密码，选择运营商后即可自动认证，支持设备下线（根据提示输入即可）

可自动判别登录情况，引导用户交互。


### 目前支持的网络类型：
````
有线网络（认证IP地址:121.251.251.207)

无线网络(SSID: UPC, 认证IP地址:121.251.251.217)

802.1X网络无需使用本脚本

````

用户信息显示等功能请等待后续更新 (逃

### 版权信息
````
Author：EndangeredFish

Email: zwy346545141@gmail.com

First Commit Date:  Monday,13 Nov 2017 

LICENSE: AGPLv3
````