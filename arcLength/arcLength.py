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

def bezierLength(curveInfo):

    FUNCTION = partial(bezierLengthFun, curveInfo = curveInfo)

    s = gauss_integral(0, 1, FUNCTION, 4)

    return s

if __name__ == "__main__":

    pnt1 = point(-165.7819, 54.22869)
    pnt2 = point(-118.0437, 148.7052)
    pnt3 = point(-55.30936, 64.97601)
    pnt4 = point(1.379291, 131.9593)

    controlPnt = np.array([pnt1, pnt2, pnt3, pnt4])

    curveInfo = bezier(3, controlPnt)

    s = bezierLength(curveInfo)
    print(s)