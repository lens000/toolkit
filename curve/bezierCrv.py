#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/11/2019 12:46 AM
# @Author  : Lens
# @Version : 3.7
# @File    : bezierCrv.py
# @Software: PyCharm


import numpy as np

from curve.curvInfo import point, nurbCurve


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

    firstCurve = np.array([])
    secondCurve = np.array([])

    firstCurve = np.append(firstCurve, pntLst[0])
    secondCurve = np.append(secondCurve, pntLst[len(pntLst) - 1])

    secondDer = None
    for i in range(n):
        if i == n-1:
            firstDer_x = pntLst[1].x - pntLst[0].x
            firstDer_y = pntLst[1].y - pntLst[0].y

            firstDer_x = firstDer_x * n
            firstDer_y = firstDer_y * n
            firstDer = point(firstDer_x, firstDer_y)

            x = t * pntLst[1].x + (1 - t) * pntLst[0].x
            y = t * pntLst[1].y + (1 - t) * pntLst[0].y
            pnt = point(x, y)

            firstCurve = np.append(firstCurve, pnt)
            secondCurve = np.append(secondCurve, pnt)
        else:
            if n >= 2 and i == n - 2:
                secondDer_x = pntLst[2].x - 2 * pntLst[1].x + pntLst[0].x
                secondDer_y = pntLst[2].y - 2 * pntLst[1].y + pntLst[0].y

                secondDer_x = n * (n -1) * secondDer_x
                secondDer_y = n * (n -1) * secondDer_y

                secondDer = point(secondDer_x, secondDer_y)

            for j in range(len(pntLst)-1):
                x = t * pntLst[j+1].x + (1-t) * pntLst[j].x
                y = t * pntLst[j+1].y + (1-t) * pntLst[j].y

                pnt = point(x,y)
                tempPnt = np.append(tempPnt, pnt)

                if j == 0:
                    firstCurve = np.append(firstCurve, pnt)

                if j == len(pntLst)-2:
                    secondCurve = np.append(secondCurve, pnt)

            pntLst = tempPnt
            tempPnt = np.array([])

    secondCurve = secondCurve[::-1]

    return pnt, firstDer,secondDer,firstCurve, secondCurve

def extendBezierCrv(curveInfo, t):

    pntLst = curveInfo.controlPnt

    if t < 0:
        pntLst = pntLst[::-1]
        t = np.fabs(t)

    degree = curveInfo.degree

    extendCrv = np.array([])

    if degree+1 != len(pntLst):
        return None

    for i in range(degree):
        if i == 0:
            x = pntLst[0].x
            y = pntLst[0].y
            pnt = point(x, y)
            extendCrv = np.append(extendCrv, pnt)
        tempPnt = np.array([])

        for j in range(len(pntLst) - 1):
            x =  pntLst[j].x + 1 / (t - 1) *(pntLst[j+1].x - pntLst[j].x)
            y =  pntLst[j].y + 1 / (t - 1) *(pntLst[j+1].y - pntLst[j].y)

            pnt = point(x, y)
            tempPnt = np.append(tempPnt, pnt)

            if j == 0:
                extendCrv = np.append(extendCrv, pnt)

        pntLst = tempPnt

    return extendCrv

def upgradeBezierDegree(curveInfo):

    pntLst = curveInfo.controlPnt
    degree = curveInfo.degree

    crvPntLst = np.array([])
    crvPntLst = np.append(crvPntLst, pntLst[0])

    for i in range(len(pntLst) - 1):
        alpha = (i+1) / (degree + 1)
        x = (pntLst[i].x * alpha + pntLst[i + 1].x) / (1 + alpha)
        y = (pntLst[i].y * alpha + pntLst[i + 1].y) / (1 + alpha)

        pnt = point(x, y)
        crvPntLst = np.append(crvPntLst, pnt)

    crvPntLst = np.append(crvPntLst, pntLst[len(pntLst) - 1])

    newCrveInfo = nurbCurve(crvPntLst, degree + 1)
    return newCrveInfo

if __name__ == "__main__":
    pnt1 = point(0, 0)
    pnt2 = point(0, 100)
    pnt3 = point(100, 100)
    pnt4 = point(100, 0)

    controlPnt = np.array([pnt1, pnt2, pnt3, pnt4])

    curveInfo = bezier(3, controlPnt)

    extendCrv = extendBezierCrv(curveInfo, 1.5)
    print(extendCrv)

    extendCrv = extendBezierCrv(curveInfo, -1.5)
    print(extendCrv)

    upgradeCrv = upgradeBezierDegree(curveInfo)
    print(upgradeCrv)
