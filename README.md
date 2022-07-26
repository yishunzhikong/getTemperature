# 获取城市温度表格

* 本脚本获取[天气网](https://www.tianqi.com/)某城市一段时间最高/最低温度数据，并写入excel表格
* 城市和起止时间再脚本里更改
import os
* 本脚本用到 `requests` 、 `re` 、 `time` 、 `os` 、 `datetime` 、 `openpyxl` 库，请提前安装