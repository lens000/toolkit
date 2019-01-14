#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/11/2019 12:46 AM
# @Author  : Lens
# @Version : 3.7
# @File    : bezier.py
# @Software: PyCharm


import numpy as np

class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class nurbCurve(object):
    def __init__(self, controlPnt, degree):
        self.degree = degree
        self.controlPnt = controlPnt
        self.curveType = None


def fac(n):
    if n < 0:
        return None
    if n <= 1:
        return 1
    return n*fac(n-1)


def bernstein(n, j, t):
    cnj = np.float(fac(n)) / (fac(j) * fac(n-j))
    base = np.power(t, j) * np.power(1-t, n-j)
    b = cnj * base
    return b

def bernsteinMatrix(n, t):

    bMat = np.array([])
    for ti in t:
        bRow = np.array([])

        for ji in range(n+1):
            bjt = bernstein(n, ji, ti)
            bRow = np.append(bRow, bjt)

        bMat = np.append(bMat, bRow)

    bMat = bMat.reshape(len(t), n+1)

    return bMat

def bezier(n, pntLst):

    if n+1 != len(pntLst):
        return None

    curve = nurbCurve(pntLst, n)
    return curve

def bezierCurve(bezierInfo, t=None, segNum=3):

    pntLst = bezierInfo.controlPnt
    n = bezierInfo.degree

    bMat = None
    if t is None:
        offset = 1.0 / (segNum - 1)
        t = np.arange(0, 1.0, offset)
        t = np.append(t, 1.0)

    bMat = bernsteinMatrix(n, t)

    xLst = np.array([])
    yLst = np.array([])

    for pnt in pntLst:
        xLst = np.append(xLst, pnt.x)
        yLst = np.append(yLst, pnt.y)

    pxLst = np.dot(bMat, xLst)
    pyLst = np.dot(bMat, yLst)

    bPntLst = zip(pxLst, pyLst)

    pntLst = [[pnt[0], pnt[1]] for pnt in bPntLst]
    pntLst = np.array(pntLst)
    return pntLst

def decasteljaus(curveInfo, t):

    pntLst = curveInfo.controlPnt
    n = curveInfo.degree

    if n+1 != len(pntLst):
        return None

    if t < 0:
        return None

    tempPnt = np.array([])

    firstDer = None
    pnt = None

    for i in range(n):
        if i == n-1:
            firstDer_x = pntLst[1].x - pntLst[0].x
            firstDer_y = pntLst[1].y - pntLst[0].y
            firstDer = point(firstDer_x, firstDer_y)

            x = t * pntLst[1].x + (1 - t) * pntLst[0].x
            y = t * pntLst[1].y + (1 - t) * pntLst[0].y
            pnt = point(x, y)
        else:
            for j in range(len(pntLst)-1):
                x = t * pntLst[j+1].x + (1-t) * pntLst[j].x
                y = t * pntLst[j+1].y + (1-t) * pntLst[j].y

                pnt = point(x,y)
                tempPnt = np.append(tempPnt, pnt)

            pntLst = tempPnt
            tempPnt = np.array([])

    return pnt, firstDer


if __name__ == "__main__":
    pnt1 = point(0, 0)
    pnt2 = point(0, 50)
    pnt3 = point(50, 50)

    controlPnt = np.array([pnt1, pnt2, pnt3])

    curveInfo = bezier(2, controlPnt)
    bPnts = bezierCurve(curveInfo, None, 5)

    pnt = decasteljaus(curveInfo, 0.3)
    print(pnt[0].x, pnt[0].y)
    print(pnt[1].x, pnt[1].y)