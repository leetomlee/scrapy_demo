import os, re

import time
from selenium import webdriver
#
# a = "2013-10-10 23:40:00"
# # a = "2013/10/10 23:40:00"
#
# timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
#
# otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
# print(otherStyleTime)
# url="http://www.xm1155.com/sj/play-26720-0-1.html"
#
# chrome = webdriver.Chrome()
# chrome.get(url)
# selector = chrome.find_element_by_css_selector("#ckplayer_a1 source::attr(src)")
# chrome.close()
# print(selector)
# import uuid
#
# uuid_ = uuid.uuid4()
# print(uuid_)
import sys
from PyQt5 import QtCore, QtWidgets

# app = QtWidgets.QApplication(sys.argv)
# widget = QtWidgets.QWidget()
# widget.resize(1000, 400)
# widget.setWindowTitle("Hello World!")
# widget.show()
#
# exit(app.exec_())
data = {"乱伦文学": "LLWX",
        "武侠古典": "WXGD",
        "淫色人妻": "YSRQ",
        "激情文学": "JQWX",
        "迷情校园": "MQXY",
        "性爱技巧": "XAJQ",
        "另类小说": "LLXS"}
print(data.get("LLWX"))
