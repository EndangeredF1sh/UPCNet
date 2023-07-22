# 中国石油大学（华东）校园网络认证脚本

![飞天面条教保佑你的代码](https://cdn.rawgit.com/LunaGao/BlessYourCodeTag/master/tags/ramen.svg)

### Openwrt路由器自动安装
在命令行中使用root权限运行以下代码即可
不自动安装curl
````shell
wget --no-check-certificate https://raw.githubusercontent.com/how1ewu/UPCNet/bash/autoinstallNoUpdate.sh && chmod +x autoinstallNoUpdate.sh && sh autoinstallNoUpdate.sh
````
自动安装curl
````shell
wget --no-check-certificate https://raw.githubusercontent.com/how1ewu/UPCNet/bash/autoinstall.sh && chmod +x autoinstall.sh && sh autoinstall.sh
````
### Openwrt路由器配置IPV6中继Relay
> 引用自[Yumao's Blog](https://www.yumao.name/read/openwrt-ipv6-bridge-or-nat6/)
LUCI界面中LAN接口设置：
```
路由通告服务：中继
DHCPv6服务：中继
NDP代理：中继
```
检查/etc/config/dhcp文件中，lan的相关参数
```
config dhcp 'lan' 
    option ra "relay"
    option dhcp "relay"
    option ndp "relay"
```
修改 /etc/config/dhcp文件中，wan的相关参数
```
config dhcp 'wan'
    option interface 'wan' 
    option dhcpv6 'relay' 
    option ra 'relay' 
    option ndp 'relay' 
    option master '1' 

```
添加计划任务
```shell
* * * * * /root/ipv6-bridge.sh
```
/root/ipv6-bridge.sh如下：
```shell
#!/bin/sh
if [ -n "`ip -6 route show default|grep from -m 1`" ];then
    logger -t "IPV6" change default gateway without from source
    DEFAULT=`ip -6 route show default|grep from -m 1`
    #刪除默認路由
    ip -6 route del ${DEFAULT}
    #添加無from source路由
    ip -6 route add `echo ${DEFAULT}|sed -e 's/from [^ ]* //'`
    #添加子網内設備通過br-lan訪問
    ip -6 route add `echo ${DEFAULT}|grep from|awk '{printf $3}'` dev br-lan metric 128
fi
#刪除之前自動添加的錯誤路由 
ip -6 route list|grep -v default|grep -v br-lan|grep static|while read -r s; do ip -6 route del $s; done
#可選：可以根據需求自定義SUBNETEX的值，UPC校园网为240c
SUBNETEX="240c:"
ip -6 route list|grep -v default|grep -v br-lan|grep ${SUBNETEX}|while read -r s; do ip -6 route del $s; done

```
```shell
chmod +x /root/ipv6-bridge.sh
```
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

Email: im.EndangeredFish@gmail.com

First Commit Date:  Monday,1 October 2018 

LICENSE: AGPLv3
````
