import requests
import re
import os
import time
import datetime
import openpyxl
from openpyxl import load_workbook

#必改数据
#查询城市
City = "beijing"
#查询开始&结束时间
timeBegin = "20220720"
timeEnd = "20220725"

# URL常量
website = "https://www.tianqi.com"
Temperature = '<span>(-?[0-9]*?)~(-?[0-9]*?)°</span>'
UserAgent = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/99.0.4844.84 Safari/537.36'
             }

#获取某个城市某天温度
def getTemp( city, date):
    s = requests.session()
    rs = s.get(website + "/tianqi/" + city + "/" + date + ".html", headers=UserAgent)
    temp = re.search(Temperature, rs.text, re.S)
    return date,int(temp.group(1)),int(temp.group(2))

#获取某个城市某段时间温度
def getTemps(city, timebegin, timeend):

    begin = datetime.date( \
        int(timebegin[0:4]), \
        int(timebegin[4:6]), \
        int(timebegin[6:8]))
    end = datetime.date( \
        int(timeend[0:4]), \
        int(timeend[4:6]), \
        int(timeend[6:8]))
    delta = datetime.timedelta(days=1)
    temps = []

    while begin <= end:
        nowdate = begin.strftime("%Y%m%d")
        temps.append(getTemp( City, nowdate))
        begin += delta
    
    return temps

# 主函数
if __name__ == '__main__':

    i = 2

    #打开excel表格
    temps = getTemps( City, timeBegin, timeEnd)
    tempWb = openpyxl.Workbook()
    tempWs = tempWb.active
    
    #写入表头
    tempWs.cell(1, 1, value="date")
    tempWs.cell(1, 2, value="min")
    tempWs.cell(1, 3, value="max")

    #将数据写入excel表格
    for tp in temps:
        tempWs.cell(i, 1, value=tp[0])
        tempWs.cell(i, 2, value=tp[1])
        tempWs.cell(i, 3, value=tp[2])
        i += 1

    #保存表格文件
    tempWb.save(City + "_" + timeBegin + "_" +timeEnd + ".xlsx")