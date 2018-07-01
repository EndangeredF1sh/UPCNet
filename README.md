# 中国石油大学（华东）校园网络认证脚本


### 源码依赖
&emsp;&emsp;采用Python3编写，依赖于

```
requests
urllib/urllib.parse
base64
```

### 使用方法

#### &emsp;upcnet.py:

如果根目录下没有账号信息就会要求输入账号密码以及选择运营商，然后会加密后保存在本地的`config.ini`文件中。值得一提的是输入密码时是不可见的，可能大部分Windows用户都不知道。

如果想要删掉保存在本地的账号可以执行`python3 upcnet.py reset`或删除根目录下的`config.ini`。

运营商对应编号：

```
1.校园网
2.联通
3.移动
4.电信
5.校园内网
```

#### &emsp;denet.py:

执行一下之后就会退出当前已登录的校园网账号。

### 目前支持的网络类型：

理论上支持所有锐捷`eportal`认证。

### 版权信息

```
Author：LucienShui

From：EndangeredFish
```

### 鸣谢

[EndangeredFish](https://github.com/EndangeredF1sh)
