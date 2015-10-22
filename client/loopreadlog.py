#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: lihongyuan
@license: Apache Licence 
@contact: 917689356@qq.com
@software: PyCharm Community Edition
@file: loopreadlog.py.py
@time: 10/14/15 11:40 AM
"""

import ConfigParser, time
from pretransactionlog import transactionlog
from logclient import SendDataToServer

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
                return filename, timekick,serveraddress,serverport
            except IOError as err:
                print 'Failed to find config items, %s' %(str(err))
    except IOError as err:
         print 'Failed open config files, %s' %(str(err))

#获取配置文件中的日志路径和读取的时间

file_name, time_kick, server_address, server_port = get_file_name()
print get_file_name()
#获取要监控的日志的文件结尾
def get_file_end(file_name):

        f = file(file_name, 'r')
        f.seek(0, 2)
        file_size = f.tell()
        f.close()
        return file_size

#根据获取的文件位置符开始读取文件内容
def get_content(file_name, last_file_size):

    f = file(file_name, 'r')
    f.seek(last_file_size, 0)
    lines = f.readlines()
    for line in lines:
        #对读取的日志记录进行处理按行
        data = transactionlog(line)
        if data is not None:
            #发送处理的日志到服务端，JSON格式
            send_data_server(data)
    f.close()

file_size = get_file_end(file_name)

last_file_size = file_size
connection = SendDataToServer(server_address,int(server_port))

def send_data_server(data):
    connection.send2server(data)

if __name__ == '__main__':
    while True:

        file_size = get_file_end(file_name)

        if file_size > last_file_size:
            print "file read start!"
            get_content(file_name, last_file_size)
        else:
            print "file not change!"
        last_file_size = file_size

        time.sleep(int(time_kick))