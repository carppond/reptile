# -*- coding = utf-8 -*-
# @Time : 2022/5/17 11:27 AM
# @Author: YL
# @File : bs4test.py
# @Software : PyCharm

from bs4 import BeautifulSoup
import re
file = open("./baidu.html", "rb")
html = file.read()

bs = BeautifulSoup(html, "html.parser")
# print(bs.title)
# print(bs.a)
# print(bs.head)
# print(bs)
# 文档的遍历
# for child in bs.body.children:
#   print(child)

# t_list = bs.findAll('a')
# for item in t_list:
#     print(item)

# t_list = bs.findAll(re.compile('a'))
# print(t_list)

# t_list = bs.findAll(text=re.compile('\\d'))
# print(t_list)

# t_list = bs.findAll('a', limit=3)
a = bs.select('title')
print(a)
