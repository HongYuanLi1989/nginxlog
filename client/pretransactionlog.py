#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: lihongyuan
@license: Apache Licence 
@contact: 917689356@qq.com
@software: PyCharm Community Edition
@file: pretransactionlog.py
@time: 10/14/15 12:26 PM
"""
import json,time,re
from logformat import log_info
from logformat import log_info2dict

def parsetime(date, month, year, log_time):
    time_str = '%s%s%s %s' % (year, month, date, log_time)
    return time.mktime(time.strptime(time_str, '%Y%b%d %H:%M:%S'))


def transactionlog(lines):
    
    ipP = r"?P<ip>[\d.]*"
    # timeP = r"""?P<time> \[[^\[\]]*\]"""
    dateP = r"?P<date>\d+"
    monthP = r"?P<month>\w+"
    yearP = r"?P<year>\d+"
    log_timeP = r"?P<time>\S+"
    timezoneP = r"?P<zone>\S+"
    requestP = r"""?P<request>\"[^\"]*\""""
    statusP = r"?P<status>\d+"
    bodyBytesSentP = r"?P<bodyByteSent>\d+"
    userAgentP = r"""?P<userAgent>\"[^\"]*\""""
    userSystems = re.compile(r'\([^\(\)]*\)')
    remoteIP = r"?P<remoteip>[\d.]*"
    upstreamAddr = r"?P<upstreamAddr>[\d.]*:[\d+]*"
    upstreamResponseTime = r"?P<ReTime>[\d.\d+]*"
    upstreamRequestTime = r"?P<requTime>[\d.\d+]*"


    nginxLogPattern = re.compile(r"(%s)\ -\ \[(%s)/(%s)/(%s)\:(%s)\ (%s)\]\ (%s)\ (%s)\ (%s)\ \"-\"\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)" %(ipP, dateP, monthP, yearP, log_timeP, timezoneP, requestP, statusP, bodyBytesSentP, userAgentP, remoteIP,upstreamAddr, upstreamResponseTime, upstreamRequestTime), re.VERBOSE)
    matchs = nginxLogPattern.match(lines)
    #print lines
    #print matchs
    if matchs != None:
        allGroup = matchs.groups()
        ip = allGroup[0]
        reqdate = allGroup[1]
        reqmonth = allGroup[2]
        reqyear = allGroup[3]
        reqtime = allGroup[4]
        reqUri = allGroup[6]
        status = allGroup[7]
        bodyBytesSent = allGroup[8]
        userAgent = allGroup[9]
        remoteAddr = allGroup[10]
        #usersystem = userSystems.findall(userAgent)

        patt = re.compile(r"\((.*?)\)", re.I|re.X)
        if userAgent == "\"-\"":
            return
        elif userAgent == "\"AHC/1.0\"":
            userAgentType = "AHC/1.0"
            AagentSystem = "AHC/1.0"
        elif remoteAddr == '119.57.35.166':
            return
        elif len(userAgent.split(' ')) == 3:
            userAgentType = 'Android'
            AagentSystem =  patt.findall(userAgent)
        elif ',' in userAgent and ';' not in userAgent:
            userAgentType = patt.findall(userAgent)[0].split(',')[1]
            AagentSystem =  patt.findall(userAgent)[0].split(',')[2]
        elif len(patt.findall(userAgent)[0].split(';')) > 3:
            print patt.findall(userAgent)[0].split(';')
            AagentSystem =  patt.findall(userAgent)[0].split(';')[2]
            userAgentType = patt.findall(userAgent)[0].split(';')[3]
        else:
            print 'iphone'
            AagentSystem =  patt.findall(userAgent)[0].split(';')[1]
            userAgentType = patt.findall(userAgent)[0].split(';')[0]

        #reqUri find
        pattUri = re.compile(r"\"(.*?)\"", re.I|re.X)
        reqUri = pattUri.findall(reqUri)
        upstreamIp = allGroup[11]
        upstreamResTime = allGroup[12]
        upstreamReqTime = allGroup[13]

        #print ip,reqdate,reqmonth,reqyear,reqtime,reqUri,status,bodyBytesSent,userAgentType,AagentSystem,remoteAddr,upstreamIp,upstreamResTime,upstreamReqTime

        #format time
        str_time = parsetime(reqdate,reqmonth,reqyear,reqtime)

        #print str_time

        logContent = log_info(ip,str_time,reqUri,status,bodyBytesSent,userAgentType,AagentSystem,remoteAddr,upstreamIp,upstreamResTime,upstreamReqTime)
        print logContent
        #print logContent
        return (json.dumps(logContent,default=log_info2dict))