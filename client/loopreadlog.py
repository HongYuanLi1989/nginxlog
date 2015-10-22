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

if __name__ == '__main__':

    file_name, time_kick, server_address, server_port = get_file_name()

    file_size = get_file_end(file_name)

    last_file_size = file_size
    connFd = createconnect(server_address,server_port)

    print connectserver(connFd,server_address,server_port)

    flag =1
    if flag == 1:
        while True:
            flag = 1
            with open("/data/logs/bak_file_1.json") as bak_f:
                lines = bak_f.readline()
                for line in lines:
                    #对读取的日志记录进行处理按行
                    data = transactionlog(line)
                    #print type(data)
                if data is not None:
                    #发送处理的日志到服务端，JSON格式
                    send2server(connFd,data)
                    #client.send_data_server(data)

            file_size = get_file_end(file_name)

            if file_size > last_file_size:
                print "file read start!"
                get_content(file_name, last_file_size,1,connFd)
            else:
                print "file not change!"
            last_file_size = file_size

            time.sleep(int(time_kick))
    else:
        while True:
            flag = 0
            file_size = get_file_end(file_name)
            print file_size
            print last_file_size
            if file_size > last_file_size:
                print "file read start!"
                get_content(file_name, last_file_size,0)
            else:
                print "file not change!"
            last_file_size = file_size
            time.sleep(int(time_kick))
