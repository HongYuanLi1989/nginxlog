#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: LiHongYuan
@contact: 917689356@qq.com
@software: PyCharm
@file: loopreadlog.py
@time: 15-10-22 下午3:17
"""
import time
from monitorclient import *
from logclient import *
from pretransactionlog import transactionlog

def createconnect(serveraddress,serverport):

    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return connFd
    except socket.error, msg:
        print msg

def processloop():

    #if __name__ == '__main__':

    file_name, time_kick, server_address, server_port = get_file_name()

    file_size = get_file_end(file_name)

    last_file_size = file_size

    connFd = createconnect(server_address,server_port)
    i = 0
    flag = 0
    while True:
        try:
            connFd.connect((server_address, int(server_port)))
            print "Connect Server Success"
            flag = 1
            break
        except socket.error, msg:
            i = i + 1
            time.sleep(5)
            flag = 0
            if i > 3:
                print "Connect To Server Failed"
                break

    print flag
    # flag =1
    if flag == 1:

        while True:

            with open("/data/logs/bak_file_1.json") as bak_f:
                lines = bak_f.readlines()
                for line in lines:
                    #对读取的日志记录进行处理按行
                    print line
                    #print type(data)
                    if line is not None:
                        print line
                        #发送处理的日志到服务端，JSON格式
                        send2server(connFd, line)
            bak_file = open("/data/logs/bak_file_1.json", 'w')
            bak_file.truncate(0)
            bak_file.close()

            file_size = get_file_end(file_name)

            if file_size > last_file_size:
                print "file read start!"
                get_content(file_name, last_file_size, 1, connFd)
            else:
                print "file not change!"
            last_file_size = file_size

            time.sleep(int(time_kick))
    else:
        while True:
            file_size = get_file_end(file_name)
            print file_size
            print last_file_size
            if file_size > last_file_size:
                print "file read start!"
                get_content(file_name, last_file_size, 0, connFd)
            else:
                print "file not change!"
            last_file_size = file_size
            time.sleep(int(time_kick))



if __name__ == '__main__':
    processloop()
