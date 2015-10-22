#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: LiHongYuan
@contact: 917689356@qq.com
@software: PyCharm
@file: importdata2mysql.py
@time: 15-10-20 下午3:10
"""

import json
import ConfigParser

from ip2address import findaddress
from utils.mysqldb import MySQL


class log_info(object):
    def __init__(self,ip,str_time,reqUri,status,bodyBytesSent,userAgentType,AagentSystem,remoteAddr,upstreamIp,upstreamResTime,upstreamReqTime):
        self.ip = ip
        self.time = str_time
        self.reqUri = reqUri
        self.status = status
        self.bodyBytesSent = bodyBytesSent
        self.userAgentType = userAgentType
        self.AgentSystem = AagentSystem
        self.remoteAddr = remoteAddr
        self.upstreamIp = upstreamIp
        self.upstreamResTime = upstreamResTime
        self.upstreamReqTime = upstreamReqTime


def getMysqlConfig():
    config = ConfigParser.ConfigParser()
    try:
        with open('../server/conf/config.ini') as cfgfile:
            config.readfp(cfgfile)
            try:
                host = config.get("mysql", "host")
                password = config.get("mysql", "password")
                db = config.get("mysql","db")
                port = config.get("mysql","port")
                user = config.get("mysql","user")
                return host,password,db,port,user
            except IOError as err:
                print "Configure Item Not Found %s" %(str(err))
    except IOError as err:
        print "Configure File Not Not Found %s" %(str(err))


def dict2log_info(loginfo):
    return log_info(loginfo['ip'],loginfo['time'],loginfo['reqUri'],loginfo['status'],loginfo['bodyBytesSent'],loginfo['userAgentType'],loginfo['AgentSystem'],loginfo['remoteAddr'],loginfo['upstreamIp'],loginfo['upstreamResTime'],loginfo['upstreamReqTime'])

def process_data(recvdata):

    recvdata = json.loads(recvdata,object_hook=dict2log_info)
    #print recvdata.AgentSystem
    #print recvdata.ip,recvdata.time,recvdata.reqUri[0],recvdata.status,recvdata.bodyBytesSent,recvdata.userAgentType,recvdata.AgentSystem,recvdata.remoteAddr,recvdata.upstreamIp,recvdata.upstreamResTime,recvdata.upstreamReqTime
    items = findaddress(recvdata.remoteAddr).strip(" ").split("\t")
    #print len(items)
    if len(items) > 2:
        country = items[0]
        province = items[1]
        city = items[2]
    else:
        country = items[0]
        province = items[1]
        city = ' '
    #print country,province,city
    finaldata = {'proxy_ip':recvdata.ip,'visit_time':recvdata.time,'requri':recvdata.reqUri[0],'visit_status':recvdata.status,'bodyBytesSent':recvdata.bodyBytesSent,'userAgentType':recvdata.userAgentType,'AgentSystem':recvdata.AgentSystem,'remoteAddr':recvdata.remoteAddr,'upStreamIp':recvdata.upstreamIp,'upStreamResTime':recvdata.upstreamResTime,'upstreamReqTime':recvdata.upstreamReqTime,'country':country,'province':province,'city':city}

    insertdata = json.dumps(finaldata,encoding="utf-8",ensure_ascii=False)
    #print finaldata
    #print type(insertdata)

    insertMysql(finaldata)
def insertMysql(insertdata):
    host,password,db,port,user = getMysqlConfig()

    #print host,password,db,port,user

    n = MySQL(host,user,password,int(port))
    n.selectDb(db)
    tbname = 'nginx_log'

    n.insert(tbname,insertdata)

    n.commit()


