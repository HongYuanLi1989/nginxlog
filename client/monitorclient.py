#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: LiHongYuan
@contact: 917689356@qq.com
@software: PyCharm
@file: MonitorClient.py
@time: 15-10-22 下午3:11
"""

import ConfigParser
from logclient import *
from pretransactionlog import transactionlog

def get_file_name():
    #读取配置文件中的日志路径和读取间隔时间
    config = ConfigParser.ConfigParser()
    try:
        with open('conf/config.ini', 'r') as cfgfile:
            config.readfp(cfgfile)
            try:
                filename = config.get("filedir", "filename")
                timekick = config.get("timekick", "timekick")
                serveraddress = config.get("serveraddress", "serveraddress")
                serverport = config.get("serverport", "serverport")
                return filename, timekick, serveraddress, serverport
            except IOError as err:
                print 'Failed to find config items, %s' %(str(err))
    except IOError as err:
         print 'Failed open config files, %s' %(str(err))

 #获取要监控的日志的文件结尾
def get_file_end(file_name):

        f = file(file_name, 'r')
        f.seek(0, 2)
        file_size = f.tell()
        f.close()
        return file_size


#根据获取的文件位置符开始读取文件内容
def get_content(file_name, last_file_size,flag,connFd):

    f = file(file_name, 'r')
    f.seek(last_file_size, 0)
    lines = f.readlines()
    for line in lines:
        #对读取的日志记录进行处理按行
        data = transactionlog(line)
        #print type(data)
        if data is not None and flag == 1:
            #发送处理的日志到服务端，JSON格式
            send2server(connFd,data)
        elif data is not None:
            write_file(data)
            print data
    f.close()

def write_file(data):

    with open("/data/logs/bak_file_1.json","a+") as f_b:
        #data = json.loads(data)
        f_b.write(data+'\n')
        print "wirte to file:%s" %data
