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


def createconnect(serveraddress,serverport):

    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return connFd
    except socket.error, msg:
        print msg

def processloop():

    #if __name__ == '__main__':
    #获取配置文件中的配置信息

    file_name, time_kick, server_address, server_port = get_file_name()
    #获取文件的结尾位置点
    file_size = get_file_end(file_name)
    #最后一次获取文件的位置点
    last_file_size = file_size

    connFd = createconnect(server_address, server_port)
    i = 0
    flag = 0
    while True:
        try:
            #尝试连接服务器，如果失败三次，退出循环
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

    # print flag
    # flag =1
    if flag == 1:

        while True:
            #读取存储在本地的处理结果
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

            #读取结束后清空本地的文件
            bak_file = open("/data/logs/bak_file_1.json", 'w')
            bak_file.truncate(0)
            bak_file.close()
            #再次获取当前的文件位置
            file_size = get_file_end(file_name)
            #如果当前的位置点大于最近的一次位置点，读取日志文件，并处理
            if file_size > last_file_size:
                print "file read start!"
                get_content(file_name, last_file_size, 1, connFd)

            else:
                print "file not change!"
            #更新最后一次获取的文件位置点
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

#向服务器发送处理结果的函数
def send2server(connFd, data):
    #如果数据发送正常，什么也不做
    if connFd.send(data):
        pass
    else:
        print "Message Send Failed!"

        #关闭连接
        connect_close(connFd)

        #connFd = ''
        #重新调用主函数
        processloop()

    readData = connFd.recv(1024)

    print readData

def connect_close(connFd):

    connFd.close()

if __name__ == '__main__':
    processloop()
