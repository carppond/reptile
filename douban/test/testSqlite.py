# -*- coding =utf-8 -*-
# @Time : 2022/5/18 10:36 PM
# @Author : YL
# @File: testSqlite.py
# @Software : PyCharm

import sqlite3

# # 打开或创建数据库文件
# connect = sqlite3.connect("test.db")
# print("成功打开数据库")
# # 获取游标
# cursor = connect.cursor()
# # 执行 sql
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char[50],
#         salary real);
# '''
# # 执行 sql
# cursor.execute(sql)
# # 提交数据库操作
# connect.commit()
# # 关闭数据库连接
# connect.close()
# print("成功建表")

# 3. 插入进去
# 打开或创建数据库文件
connect = sqlite3.connect("test.db")
print("成功打开数据库")
# 获取游标
cursor = connect.cursor()
# 执行 sql
sql = "select id, name, age,address,salary from company"
# 执行 sql
cursorData = cursor.execute(sql)
for row in cursorData:
    print("id = ",row[0])
    print("name = ", row[1])
    print("age = ", row[2])
    print("address = ", row[3])
    print("salary = ", row[4], "\n")
# 关闭数据库连接
connect.close()
print("查询完毕")