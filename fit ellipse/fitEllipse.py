#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 20:35
# @Author  : Lens
# @Site    : 
# @File    : fitEllipse.py
# @Software: PyCharm

import numpy as np
import scipy


class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def param2Geom(p):
    A = p[0]
    B = p[1]
    C = p[2]
    D = p[3]
    E = p[4]
    F = p[5]

    temp1 = np.power(B, 2) - 4 * A * C
    temp2 = np.power(A-C, 2) + np.power(B, 2)
    temp2 = np.sqrt(temp2)

    temp3 = A * np.power(E, 2) + C*np.power(D, 2) - B*D*E + temp1 * F
    temp4 = A + C

    a = temp3 * (temp4 + temp2)
    a = - np.sqrt(2 * a) / temp1

    b = temp3*(temp4 - temp2)
    b = - np.sqrt(2*b) / temp1

    xc = (2 *C*D - B*E) / temp1
    yc = (2*A*E - B*D) / temp1

    theta = 0
    if B == 0 and A < C:
        theta = 0
    elif B == 0 and A >C:
        theta = np.pi / 2
    else:
        theta = np.arctan2(C-A-temp2, B)

    if a < b:
        a,b = b, a
        theta = theta - np.sign(theta)*np.pi/2
    return np.array([a, b, xc, yc, theta])

def geom2Param(g):
    a = g[0]
    b = g[1]
    xc = g[2]
    yc = g[3]
    theta = g[4]

    A = np.power(a*np.sin(theta), 2) + np.power(b*np.cos(theta), 2)
    B = 2*(np.power(b, 2) - np.power(a, 2))*np.sin(theta)*np.cos(theta)
    C = np.power(a*np.cos(theta), 2) + np.power(b*np.sin(theta), 2)
    D = -2*A*xc - B*yc
    E = -B*xc - 2*C*yc
    F = A*np.power(xc, 2) + B * xc * yc + C*np.power(yc, 2) - np.power(a*b, 2)
    return np.array([A, B, C, D, E, F])

def desigenMat(PntLst):
    mat1 = []
    mat2 = []

    for pnt in PntLst:
        rowElem1 = [pnt.x*pnt.x, pnt.x*pnt.y, pnt.y*pnt.y]
        mat1.append(rowElem1)

        rowElem2 = [pnt.x, pnt.y, 1]
        mat2.append(rowElem2)

    D1 = np.array(mat1)
    D2 = np.array(mat2)

    s1 = D1.transpose().dot(D1)
    s2 = D1.transpose().dot(D2)
    s3 = D2.transpose().dot(D2)

    return s1, s2, s3

def findMinPos(eigenVector):
    minId = -1
    minValue = -1.0e-12
    for i in range(len(eigenVector)):
        a, b, c = eigenVector[:,i]
        res = 4*a*c - b*b
        if res > 1.0e-12:
            if minValue < res:
                minValue = res
                minId = i
    return  minId

def fitEllipse(pntLst):

    s1, s2, s3 = desigenMat(pntLst)

    c = np.zeros((3, 3))
    c[0][2] = 2
    c[1][1] = -1
    c[2][0] = 2

    T = -np.linalg.inv(s3).dot(s2.transpose())
    M = s1 + s2.dot(T)
    cinv = np.linalg.inv(c)
    M = cinv.dot(M)

    eigen = np.linalg.eig(M)
    eigenvalue = eigen[0]
    eigenvector = eigen[1]

    minPosIdx = findMinPos(eigenvector)

    if minPosIdx < 0:
        return None

    a1 = eigenvector[:, minPosIdx]
    a2 = T.dot(a1)
    a = np.append(a1, a2)
    g = param2Geom(a)

    return g

if __name__ == "__main__":
    pnt1 = point(0.241596, 0.4851885 )
    pnt2 = point(-0.7056844, 0.3542631)
    pnt3 = point(-0.7056811, -0.3542648)
    pnt4 = point(0.2416062, -0.4851872)
    pnt5 = point(1, 0)

    pntLst = np.array([pnt1, pnt2, pnt3, pnt4,pnt5])

    g = fitEllipse(pntLst)
    print(g)
