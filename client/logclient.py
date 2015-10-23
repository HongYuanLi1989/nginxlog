#!/usr/bin/env python
# coding: utf-8


"""
@version: 1.0
@author: lihongyuan
@license: Apache Licence
@contact: 917689356@qq.com
@software: PyCharm Community Edition
@file: logclient.py
@time: 10/14/15 12:27 PM
"""
import socket
from loopreadlog import processloop

def send2server(connFd,data):

    if connFd.send(data) != len(data):
        print "Message Send Failed!"
        return processloop()

    readData = connFd.recv(1024)

    print readData

def connect_close(connFd):
    connFd.close()