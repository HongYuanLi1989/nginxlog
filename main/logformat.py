#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: lihongyuan
@license: Apache Licence 
@contact: 917689356@qq.com
@software: PyCharm Community Edition
@file: logformat.py
@time: 10/14/15 12:27 PM
"""

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

def log_info2dict(loginfo):
    return {
        'ip' : loginfo.ip,
        'time' : loginfo.time,
        'reqUri' : loginfo.reqUri,
        'status' : loginfo.status,
        'bodyBytesSent' : loginfo.bodyBytesSent,
        'userAgentType' : loginfo.userAgentType,
        'AgentSystem' : loginfo.AgentSystem,
        'remoteAddr' : loginfo.remoteAddr,
        'upstreamIp' : loginfo.upstreamIp,
        'upstreamResTime' : loginfo.upstreamResTime,
        'upstreamReqTime' : loginfo.upstreamReqTime
    }