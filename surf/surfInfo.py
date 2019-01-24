#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/24/2019 3:41 PM
# @Author  : Lens
# @Version : 3.7
# @File    : surfInfo.py
# @Software: PyCharm

from curve.curvInfo import *

class nurbSurf(object):
    def __init__(self, controlPnts, udegree, vdegree, dim, type = None):
        self.cp = controlPnts
        self.udegree = udegree
        self.vdegree = vdegree
        self.dim = dim
        self.type = type



