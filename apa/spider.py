# -*- coding = utf-8 -*-
# @Time : 2022/5/20 10:43 AM
# @Author: YL
# @File : spider.py
# @Software : PyCharm
import os
import urllib.request
import urllib.error
import urllib.parse
import json

cookie = "SERVERID=a3644fed3701a8466e8ab8ae499e8b91|1653025493|1653025461"

def getHeaders():
    headers = {
        "cookie": cookie,
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJHVUlEIjoiMjE3OTEyMTQyNzQwNDEzY2FmOWFlMDUyN2JjMjhlM2YiLCJOU1BsYXRmb3JtVHlwZSI6MiwiVXNlclR5cGUiOjQsIlVpZCI6MTAzMDU3LCJOYW1lIjoiMTgxNDM0MDYyODAiLCJSZWFsTmFtZSI6IuadjuaIkOemjzIy6auY5aSN5LiT5Y2H5pys6K6h566X5py656eR5a2m5LiO5oqA5pyv5paH5LiAIiwiUm9sZSI6IiIsIkRlc2NyaXB0aW9uIjoie1xyXG4gIFwibG9naW50aW1lXCI6IFwiMjAyMi0wNC0wNyAyMzowMDozMlwiLFxyXG4gIFwibG9naW5pcFwiOiBcIjExNS4xOTIuMTMzLjEwOVwiXHJcbn0iLCJjbGllbnQiOjUsImNsaWVudGlkIjoiMERDRjgyRjUtMjVGOC00RDFCLTlEMkYtMTgzQkM1NzU3ODQ5IiwiaDVfb3BlbmlkIjpudWxsLCJ4Y3hfb3BlbmlkIjpudWxsLCJ4Y3hfaW5mbyI6bnVsbCwieGN4X3Nlc3Npb25fa2V5IjpudWxsLCJoNV9pbmZvIjpudWxsLCJOU1RlYWNoZXJfSUQiOjAsIkV4cGlyYXRpb25UaW1lIjoiMjAyMy0wNC0wNyAyMzowMDozMiJ9.xBdb3G_KpvEdvkk65nSlUAu3-XrSV_ybi2UFYA1Aq78",
        "user-agent": "LiveClassroom/2.3.3 (iPhone; iOS 15.5; Scale/3.00)",
    }
    return headers

def pagerData():
    global cookie
    urlStr = r"https://api.apa.cn/api/student/course/pager"
    headers = getHeaders()
    data = {
        "class":35495,
        "page":1,
        "pagesize":20,
        "school":9528,
        "sort":-1
    }
    data = bytes(urllib.parse.urlencode(data), encoding='utf-8')
    req = urllib.request.Request(url=urlStr, headers=headers, data=data, method='POST')
    try:
        res = urllib.request.urlopen(req)
        # res = opener.open(req)
        # 更新 cookie
        for item in res.getheaders():
            if "Set-Cookie" in item:
                cookie = item[1]

        # 序列号数据
        jsonStr = res.read().decode('utf-8')
        dict = json.loads(jsonStr)
        data = dict["data"]
        list = data["list"]
        getVideoInfo(list)

    except urllib.error.URLError as e:
        print(e.reason)

def getVideoInfo(list):
    global cookie
    downList = []
    for item in list:
        idr = item["id"]

        urlStr = r"https://api.apa.cn/api/student/course/video/info"
        headers = getHeaders()
        data = {"id": idr}
        data = bytes(urllib.parse.urlencode(data), encoding='utf-8')
        req = urllib.request.Request(url=urlStr, headers=headers, data=data, method='POST')
        try:
            res = urllib.request.urlopen(req)
            # res = opener.open(req)
            # 更新 cookie
            for header in res.getheaders():
                if "Set-Cookie" in header:
                    cookie = header[1]

            # 序列号数据
            jsonStr = res.read().decode('utf-8')
            dict = json.loads(jsonStr)
            data = dict["data"]
            for video in data:
                downList.append(video)
        except urllib.error.URLError as e:
            print(e.reason)
    # length = int(len(downList))
    # downList = downList[length-2: length]
    # print(downList[length-2: length])
    downvideo(downList)

class url_mp4():
    def __init__(self, url, filename="default.mp4"):
        self.url = url
        download_path = os.getcwd() + r"\download/"
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        self.filename = download_path + filename

    def Schedule(self, a, b , c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 1
        print("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r')

    def download(self):
        try:
            print("\"" + self.filename + "\"" + "已经开始下载")
            urllib.request.urlretrieve(self.url, self.filename, reporthook=self.Schedule)
            print("\"" + self.filename + "\"" + "已经下载完成")
        except Exception as e:
            print("下载失败")
            print(e)
    def run(self):
        self.download()

def downvideo(downlist):
    for video in downlist:
        headers = getHeaders()
        video_url = video["mp4"]
        title = video["title"]
        filename = title + '.mp4'
        mp4 = url_mp4(url=video_url, filename=filename)
        mp4.run()

if __name__ == "__main__":
    pagerData()
