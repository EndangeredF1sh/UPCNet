# 中国石油大学（华东）校园网络认证脚本

![飞天面条教保佑你的代码](https://cdn.rawgit.com/LunaGao/BlessYourCodeTag/master/tags/ramen.svg)

### Openwrt路由器自动安装
在命令行中使用root权限运行以下代码即可
````
wget --no-check-certificate https://raw.githubusercontent.com/EndangeredF1sh/UPCNet/bash/autoinstall.sh && chmod +x autoinstall.sh && sh autoinstall.sh
````

### 手动安装方法（其他Linux发行版，暂不支持pandavan）
在UPCNet.sh文件下输入学号(username)、密码(password)和运营商编号(service)，然后运行
```
bash UPCNet.sh
```

运营商对应编号：

```
default -> 校园网
unicom -> 联通
cmcc -> 移动
ctcc -> 电信
local -> 校园内网
```

在计划任务中加入定时启动
```
crontab -e
在首行插入
*/1 * * * * sh ~/UPCNet.sh
```

### 依赖
本脚本采用Bash编写，依赖于
````
cURL
````
大部分Linux都自带cURL，如果遇上
```
curl:command not found
```
则需自行搜索安装cURL

### 支持的操作系统
```
各Linux发行版
OpenWrt/LEDE等Linux衍生系统
```
padavan似乎无法兼容（路径不同）。


### 支持的网络类型：
````
有线网络（认证IP地址:121.251.251.207)
````

### 测试环境
```
OpenWrt 15.05.1 r49587
```

### 版权信息
````
Author：EndangeredFish

Email: zwy346545141@gmail.com

First Commit Date:  Monday,1 October 2018 

LICENSE: AGPLv3
````
