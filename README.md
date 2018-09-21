# 中国石油大学（华东）校园网络认证脚本


## 源码依赖
采用Python3编写，依赖于

```
requests
urllib/urllib.parse
base64
```

## 使用方法

### upcnet.py

如果根目录下没有账号信息就会要求输入账号密码以及选择运营商，然后会加密后保存在本地的`config.ini`文件中，可能需要提醒一下的是输入密码时输入的字符是不可见的。

```
python3 upcnet.py # 初次使用，初始化参数
python3 upcnet.py reset # 删除config.ini，即本地已有的账号信息
python3 upcnet.py logout # 退出当前登录的账号
```

运营商对应编号：

```
1.校园网
2.联通
3.移动
4.电信
5.校园内网
```

## 目前支持的网络类型：

理论上支持所有锐捷`eportal`认证。

## 版权信息

```

Author: [EndangeredFish](https://github.com/EndangeredF1sh)
Refactor: [LucienShui](https://github.com/LucienShui)

```
