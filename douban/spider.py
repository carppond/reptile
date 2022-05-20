# -*- coding = utf-8 -*-
# @Time : 2022/5/17 9:13 AM
# @Author: YL
# @File : spider.py
# @Software : PyCharm

import re  # 正则匹配
import sqlite3  # 进行 sqlite 操作
import urllib.request, urllib.error  # 制定url，获取网页数据
import xlwt  # 进行 excel 操作
from bs4 import BeautifulSoup  # 网页解析，获取数据


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1. 爬取数据
    datalist = getdata(baseurl)
    # savePath = ".\\豆瓣电影Top250.xls"
    dbpath = "movie.db"
    # 2. 解析数据
    # 3. 保存数据
    # saveData(datalist, savePath)
    saveDataToDB(datalist, dbpath)

# 创建正则表达式对象，表示规则，字符串匹配模式
# 找到影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')
# 找到影片图片链接的规则
find_img_link = re.compile(r'<img.*src="(.*?)".*">', re.S)  # re.s 让换行符包含在内
# 找到影片标题的规则
find_title = re.compile(r'<span class="title">(.*)</span>')
# 找到影片的评分
find_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
find_judge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
find_inq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
find_bd = re.compile(r'<p class="">(.*?)</p>', re.S)


# <img width="100" alt="肖申克的救赎" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" class="">
def getdata(baseurl):
    datalist = []

    for i in range(0, 10):
        url = baseurl + str(i * 25)
        # 保存获取到的网页源码
        html = askURL(url)
        # 2. 逐一解析
        soup = BeautifulSoup(html, "html.parser")
        index = 0
        # 查找符合要求的字符串，形成列表
        for item in soup.find_all('div', class_="item"):
            # print(item) # 测试：查看电影 item 全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)
            # 获取到影片详情的链接
            link = re.findall(findLink, item)[0]  # re 库用来通过正则表达式来查找指定字符串
            data.append(link)
            # 获取到影片图片链接
            imglink = re.findall(find_img_link, item)[0]
            data.append(imglink)
            # 获取到影片名称：中国名 外国名
            titles = re.findall(find_title, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  # 外国电影名留空

            # 获取到影片的评分
            rating = re.findall(find_rating, item)[0]
            data.append(rating)
            # 获取到影片评价人数
            judge = re.findall(find_judge, item)[0]
            data.append(judge)
            # 获取到影片简介
            inq = re.findall(find_inq, item)
            if len(inq) != 0:
                inq = inq[0]
                inq = inq.replace("。", "")  # 去掉句号
                data.append(inq)
            else:
                data.append(" ")  # 留空

            # 获取到影片内容
            bd = re.findall(find_bd, item)[0]
            bd = re.sub(r'<br(\s+)?/>', " ", bd)  # 去掉 br
            bd = re.sub("/", " ", bd)
            data.append(bd)

            datalist.append(data)
    return datalist


# 得到指定一个 url 的网页内容
def askURL(url):
    # 用户代理，告诉豆瓣服务器，是什么类型机器，浏览器。
    head = {
        # 模拟豆瓣的user-agent
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    req = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def saveData(datalist, savePath):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        worksheet.write(0, i, col[i])  # 列表
    for i in range(len(datalist)):
        print("第%d条" % (i+1))
        data = datalist[i]
        for j in range(len(data)):
            value = data[j]
            # 数据
            worksheet.write(i+1, j, value)
    # 保存数据到 xml 表哥
    workbook.save("222.xls")

def saveDataToDB(datalist, dbpath):
    db_init(dbpath)
    connect = sqlite3.connect(dbpath)
    cur = connect.cursor()

    for data in datalist:
        for index in range(len(data)):
            # 对应的第五和第六个位置是数值型
            if index == 4 or index === 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movieTop250 (
            info_link, pic_link, cname, ename, score, reted, instroduct, info
            ) values (%s)'''%(",".join(data))
        print(sql)
        cur.execute(sql)
        connect.commit()
    cur.close()
    connect.close()

def db_init(dbpath):
    # 创建数据表
    sql = '''
        create table if not exists movieTop250 
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        reted numeric,
        instroduct text,
        info text
        )
    '''
    connect = sqlite3.connect(dbpath)
    cur = connect.cursor()
    cur.execute(sql)
    connect.commit()
    cur.close()
    connect.close()

if __name__ == "__main__":
    main()
    print("爬取完毕")
