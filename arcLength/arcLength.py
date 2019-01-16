#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 20:28
# @Author  : Lens
# @Version : 3.7
# @File    : arcLength.py
# @Software: PyCharm


import numpy as np
from integral.gauss_integral import gauss_integral
from curve.bezier import decasteljaus, bezier,point
from functools import partial

def arcLength(x):
    dxu = -np.sin(x)
    dyu = np.cos(x)

    s = np.sqrt(dxu*dxu + dyu*dyu)

    return s


def bezierLengthFun(t, curveInfo):
    _,derivePnt = decasteljaus(curveInfo, t)
    dxt = derivePnt.x
    dyt = derivePnt.y
    s = np.sqrt(dxt*dxt + dyt*dyt)
    return s

def bezierLength(curveInfo, tStart = 0, tEnd = 1.0):

    FUNCTION = partial(bezierLengthFun, curveInfo = curveInfo)

    s = gauss_integral(tStart, tEnd, FUNCTION, 4)

    return s

def test():
    pnt1 = point(0,0)
    pnt2 = point(0,100)
    pnt3 = point(100,100)

    controlPnt = np.array([pnt1, pnt2, pnt3])

    curveInfo = bezier(2, controlPnt)

    t = lambda x: 200*np.sqrt(1 - 2* x + 2*x*x)
    s = gauss_integral(0, 1, t, 4)
    return s

def findParamByLength(curveInfo, length):

    s = bezierLength(curveInfo)

    if length > s or length < 0:
        return None

    if length == 0:
        return 0

    if np.fabs(length - s) < 1.0e-12:
        return 1

    end_x = 1.0
    start_x = 0
    mid_x = (end_x + start_x) / 2
    s = bezierLength(curveInfo, 0, mid_x)

    while True:
        if np.fabs(s - length) > 1.0e-12:
            if s > length:
                end_x = mid_x
                mid_x = (start_x + end_x) / 2
            else:
                start_x = mid_x
                mid_x = (start_x + end_x) / 2
            s = bezierLength(curveInfo, 0, mid_x)
        else:
            return mid_x

if __name__ == "__main__":

    pnt1 = point(0, 0)
    pnt2 = point(0, 100)
    pnt3 = point(100,100)
    pnt4 = point(100, 0)

    controlPnt = np.array([pnt1, pnt2, pnt3, pnt4])

    curveInfo = bezier(3, controlPnt)

    s = bezierLength(curveInfo)
    print(s)

    s = test()
    print(s)

    s = bezierLength(curveInfo, 0, 0.74321)
    print(s)

    t = findParamByLength(curveInfo, s)
    print(t)