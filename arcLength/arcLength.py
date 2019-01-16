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
    # I don't know why multiply degree
    return s * curveInfo.degree

def bezierLength(curveInfo, tStart = 0, tEnd = 1.0):

    FUNCTION = partial(bezierLengthFun, curveInfo = curveInfo)

    s = gauss_integral(tStart, tEnd, FUNCTION, 4)

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

    pnt1 = point(-165.7819, 54.22869)
    pnt2 = point(-118.0437, 148.7052)
    pnt3 = point(-55.30936, 64.97601)
    pnt4 = point(1.379291, 131.9593)

    controlPnt = np.array([pnt1, pnt2, pnt3, pnt4])

    curveInfo = bezier(3, controlPnt)
    print(s)

    s = bezierLength(curveInfo, 0, 0.74321)
    print(s)

    t = findParamByLength(curveInfo, s)
    print(t)