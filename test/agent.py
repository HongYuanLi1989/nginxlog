#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: LiHongYuan
@contact: 917689356@qq.com
@software: PyCharm
@file: agent.py
@time: 15-11-10 下午12:37
"""
import threading
import time
from moniItems import MonClass

class portMonitor(threading.Thread):
    def __init__(self, name, cond):
        super(portMonitor, self).__init__()
        self.name = name
        self.cond = cond
        self.count = 0
        self.dd = 0

    def run(self):
        while 1:
            mon = MonClass()
            self.cond.acquire()
            data = mon.runAllGet()
            print data
            self.cond.release()

            self.cond.acquire()
            if self.name == 'thread1':
                self.count += 1
                print "%s,%s" % (self.name, self.count)
            else:
                self.dd += 1
                print "%s,%s" % (self.name, self.dd)
            time.sleep(3)
            print self.name + "            --------waiting-----"
            self.cond.notify()
            self.cond.wait()
            print self.name + "            ========notify======"
            self.cond.release()

if __name__ == '__main__':
    cond = threading.Condition()
    thread1 = portMonitor("thread1", cond)
    thread1.start()

    thread2 = portMonitor("thread2",cond)
    thread2.start()