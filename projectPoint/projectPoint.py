#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/15/2019 12:57 AM
# @Author  : Lens
# @Version : 3.7
# @File    : projectPoint.py
# @Software: PyCharm


import numpy as np


def projectPoint(plane, pnt):

    xn = plane[0:3,0]
    yn = plane[0:3,1]
    zn = plane[0:3,2]

    po = plane[0:3,3]

    npnt =  pnt - po

    plane_mat = np.zeros((3, 3))

    plane_mat[:,0] = xn
    plane_mat[:,1] = yn
    plane_mat[:,2] = zn

    npnt = np.linalg.inv(plane_mat).dot(npnt)

    return npnt


if __name__ == "__main__":
    plane = np.eye(4)
    plane[0][3] = -100
    plane[1][3] = -100
    plane[2][3] = -100

    point = np.array([-42,-14,28])

    point = projectPoint(plane, point)
    print(point)