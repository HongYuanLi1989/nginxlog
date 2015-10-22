#!/usr/bin/python
# encoding: utf-8
"""
@version: 1.0
@author: lihongyuan
@license: Apache Licence
@contact: 917689356@qq.com
@software: PyCharm Community Edition
@file: logserver.py
@time: 10/14/15 11:40 AM
"""

import socket, select, errno
import datetime
from importdata2mysql import process_data

def format_message(strlen):
    recvtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info = 'Recv Data Success Data Size Is: %s' %strlen
    message = recvtime + ' ' + info
    return message

if __name__ == '__main__':


    try:
        listen_fd = socket.socket(socket.AF_INET,socket.SOCK_STREAM, 0)
    except socket.error, msg:
        print "Create Socket Failed"

    try:
        listen_fd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

    except socket.error, msg:

        print "Set Socketop SO_REUSEADDR Failed"

    try:
        listen_fd.bind(('', 10086))
        listen_fd.setblocking(0)
    except socket.error, msg:
        print "Bind Failed!"
    try:
        listen_fd.listen(10)
    except socket.error, msg:
        print msg
    try:
        epoll_fd = select.epoll()
        epoll_fd.register(listen_fd.fileno(),select.EPOLLIN)
    except select.error, msg:
        print msg

    connections = {}
    addresses = {}
    datalist = {}

    while True:
        epoll_list = epoll_fd.poll()

        for fd, events in epoll_list:
            if fd == listen_fd.fileno():
                conn, addr = listen_fd.accept()

                conn.setblocking(0)

                epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)

                connections[conn.fileno()] = conn
                addresses[conn.fileno()] = addr

            elif select.EPOLLIN & events:

                datas = ''
                while True:
                    try:
                        data = connections[fd].recv(10)
                        if not data and not datas:
                            epoll_fd.unregister(fd)
                            connections[fd].close()
                            break
                        else:
                            datas += data
                    except socket.error, msg:

                        if msg.errno == errno.EAGAIN:
                            datalist[fd] = datas
                            epoll_fd.modify(fd, select.EPOLLET | select.EPOLLOUT)
                            #数据处理函数
                            process_data(datalist[fd])
                            break
                        else:
                            epoll_fd.unregister(fd)
                            connections[fd].close()
                            break

            elif select.EPOLLHUP & events:
                epoll_fd.unregister(fd)
                connections[fd].close()
            elif select.EPOLLOUT & events:
                #给客户端发送接收成功消息
                # sendLen = ''
                # sendlen = str(len(datalist[fd]))
                # message = format_message(sendlen)
                #
                # connections[fd].send(message)
                # if sendLen == len(datalist[fd]):
                #     break
                sendLen = 0
                # 通过 while 循环确保将 buf 中的数据全部发送出去
                while True:
                    # 将之前收到的数据发回 client -- 通过 sendLen 来控制发送位置
                    sendLen += connections[fd].send(datalist[fd][sendLen:])
                    # 在全部发送完毕后退出 while 循环
                    if sendLen == len(datalist[fd]):
                        break
                # 更新 epoll 句柄中连接 fd 注册事件为 可读
                epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLET)
            else:
                continue
