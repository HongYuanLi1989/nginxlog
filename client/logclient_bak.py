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

def get_server_address():

    config = ConfigParser.ConfigParser()
    try:
        with open('../conf/config.ini') as cfgfile:
            config.readfp(cfgfile)
            try:
                serveraddress = config.get("serveraddress", "serveraddress")
                serverport = config.get("serverport", "serverport")
                return serveraddress,serverport
            except IOError as err:
                print "Configure Item Not Found %s" %(str(err))
    except IOError as err:
        print "Configure File Not Not Found %s" %(str(err))

def connect2server():

    serveraddress, serverport = get_server_address()

    print serveraddress,serverport

    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print msg
    try:
        connFd.connect((serveraddress, int(serverport)))
        print "Connect To Server Success"
    except socket.error,msg:
        print msg

    return connFd



def send2server(data):
    connFd = connect2server()
    if connFd.send(data) != len(data):
        print "Message Send Failed!"
        return

    readData = connFd.recv(1024)

    print readData
    # if not readData:
    #     if str(len(data)) == readData.split(":")[3].strip():
    #         print "Message Has Send Success!"
    #     else:
    #         print "Message Send failed"
    #else:
        #time.sleep(1)

    connFd.close()