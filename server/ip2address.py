#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: LiHongYuan
@contact: 917689356@qq.com
@software: PyCharm
@file: ip2address.py
@time: 15-10-20 下午4:38
"""
import IP


def findaddress(address):
    local = IP.find(address).strip(" ")
    return local