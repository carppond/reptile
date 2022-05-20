# -*- coding = utf-8 -*-
# @Time : 2022/5/18 1:09 PM
# @Author: YL
# @File : xwlttest.py
# @Software : PyCharm

import xlwt

# 1. 创建 workbook 对象
workbook = xlwt.Workbook(encoding='utf-8')
# 2. 创建工作表
worksheet = workbook.add_sheet("sheet1")
# 3. 写入数据
# 第一个参数：行
# 第二个参数：列
# 第三个参数：存储内容
worksheet.write(0, 0, 'hello')
# 4. 保存数据表
workbook.save("111.xls")

worksheet = workbook.add_sheet("sheet2")
for i in range(1, 10):
    for j in range(1, i+1):
        value = str(i) + 'x' + str(j) + '=' + str(i * j)
        worksheet.write(i-1, j-1, value)

workbook.save('111.xls')