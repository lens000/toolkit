#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/24/2019 2:56 PM
# @Author  : Lens
# @Version : 3.7
# @File    : curvInfo.py
# @Software: PyCharm

class point(object):
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z

class nurbCurve(object):
    def __init__(self, controlPnt, degree, dim = None, type = None,):
        self.degree = degree
        self.controlPnt = controlPnt
        self.curveType = type
        self.dim = dim
