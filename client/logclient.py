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
import socket,time
import ConfigParser

class SendDataToServer:
    #global connFd

    def __init__(self,serveraddress,serverport):

        self.serveraddress = serveraddress
        self.serverport = serverport
        try:
            self.connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print msg
        try:
            self.connFd.connect((self.serveraddress, int(self.serverport)))
            print "Connect To Server Success"
        except socket.error,msg:
            print msg

    # def connect2server(self):
    #     try:
    #         connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     except socket.error, msg:
    #         print msg
    #     try:
    #         connFd.connect((self.serveraddress, int(self.serverport)))
    #         print "Connect To Server Success"
    #     except socket.error,msg:
    #         print msg
    #
    #     return connFd



    def send2server(self,data):

        if self.connFd.send(data) != len(data):
            print "Message Send Failed!"
            return

        readData = self.connFd.recv(1024)

        print readData
        # if not readData:
        #     if str(len(data)) == readData.split(":")[3].strip():
        #         print "Message Has Send Success!"
        #     else:
        #         print "Message Send failed"
        #else:
            #time.sleep(1)

        self.connFd.close()