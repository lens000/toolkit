#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 22:36
# @Author  : Lens
# @Version : 3.7
# @File    : lagrange.py
# @Software: PyCharm

import numpy as np

def lagrange(xpnts, ypnts, x):

    n = 0
    if len(xpnts) != len(ypnts):
        return None

    n = len(xpnts)

    res = 0
    for i in range(n):
        Li = 1
        for j in range(n):
            if i != j:
                Li *= ((x - xpnts[j]) / (xpnts[i] - xpnts[j]))
        res += ypnts[i] * Li

    return res

def lineInterpolation(xpnts, ypnts, x):
    if len(xpnts) != 2 or len(ypnts) != 2:
        return None
    return  lagrange(xpnts, ypnts, x)


if __name__ == "__main__":
    xpnts = np.array([0, 2, 3])
    ypnts = np.array([1, 2, 4])

    res = lagrange(xpnts, ypnts, 0.5)
    print(res)

    xpnts = np.array([-80.7595,37.4684])
    ypnts = np.array([40.5063,61.0127])

    y = lineInterpolation(xpnts, ypnts, 100)
    print(y)

