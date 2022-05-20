# -*- coding = utf-8 -*-
# @Time : 2022/5/17 9:41 AM
# @Author: YL
# @File : urllibTest.py
# @Software : PyCharm

import urllib.parse
import urllib.request

# get 请求
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode('utf-8'))

# post 请求
# data = bytes(urllib.parse.urlencode({"Hello":"xxxx"}),encoding="utf-8")
# response = urllib.request.urlopen("https://httpbin.org/post",data=data)
# print(response.read().decode('utf-8'))

# 超时
# try:
#     response = urllib.request.urlopen("https://httpbin.org/get",timeout=0.1)
#     print(response.read().decode('utf-8'))
# except urllib.error.URLError as e:
#     if isinstance(e.reason, socket.timeout):
#         print("超时")
#

url = "https://movie.douban.com/top250?start=0&filter="
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}
data = bytes(urllib.parse.urlencode({"name":"咱三"}), encoding='utf-8')
req = urllib.request.Request(url=url,headers=header)

res = urllib.request.urlopen(req)
print(res.read().decode('utf-8'))
