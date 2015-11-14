#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: LiHongYuan
@contact: 917689356@qq.com
@software: PyCharm
@file: moniItems.py
@time: 15-11-10 下午12:37
"""

import json
import urllib
import inspect
import os
import time

class MonClass:

    def __init__(self):

        self.data = {}

    def getLoadAvg(self):

        with open('/proc/loadavg') as load_open:
            load_data = load_open.read().split()[:3]
            return load_data
    def getMemTotal(self):
        with open('/proc/meminfo') as mem_open:

            mem_total = int(mem_open.readline().split()[1])
            return mem_total / 1024

    def getMemUsage(self, noBufferCache=True):

        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])

                return (T-F-B-C)/1024
        else:
            with open('/proc/meminfo') as mem_open:
                M = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return M / 1024

    def getMemFree(self,noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (F + B + C) / 1024

    def getHost(self):
        return ['host1', 'host2', 'host3', 'host4', 'host5'][int(time.time() * 1000.00) % 5]

    def getTime(self):
        return int(time.time())

    def runAllGet(self):

        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            if fun[0] == "userDefineMon":

                self.data.update(fun[1]())

            elif fun[0][:3] == 'get':
                self.data[fun[0][3:]] = fun[1]()
        return self.data

if __name__ == "__main__":
    mon = MonClass()
    print mon.runAllGet()