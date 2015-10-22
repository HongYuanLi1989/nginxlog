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

def createconnect(serveraddress,serverport):

    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return connFd
    except socket.error, msg:
        print msg

def connectserver(connFd,serveraddress,serverport):
    try:
        connFd.connect((serveraddress, int(serverport)))
        print "Connect Server Success"
        flag = 1
    except socket.error,msg:
        print msg
        flag = 0
def send2server(connFd,data):

    if connFd.send(data) != len(data):
        print "Message Send Failed!"
        return

    readData = connFd.recv(1024)

    print readData

def connect_close(connFd):
    connFd.close()