#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/24/2019 3:00 PM
# @Author  : Lens
# @Version : 3.7
# @File    : bezier3dCrv.py
# @Software: PyCharm


from curve.curvInfo import point, nurbCurve
import numpy as np

def bezier3dCrv(crv3d, t):

    dim = crv3d.dim
    degree = crv3d.degree
    pntLst = crv3d.controlPnt
    type = crv3d.curveType


    if dim != 3:
        return None

    if len(pntLst) != degree + 1:
        return None

    for i in range(degree):
        tempPnt = np.array([])

        for j in range(len(pntLst)-1):
            x = t * pntLst[j + 1].x + (1 - t) * pntLst[j].x
            y = t * pntLst[j + 1].y + (1 - t) * pntLst[j].y
            z = t * pntLst[j + 1].z + (1 - t) * pntLst[j].z

            pnt = point(x, y, z)
            tempPnt = np.append(tempPnt, pnt)

        pntLst = tempPnt
    return pntLst[0]


if __name__ == "__main__":
    pnt1 = point(-41.88438, 41.26041, 49.91586)
    pnt2 = point(-73.06837, 13.91201, 87.07949)
    pnt3 = point(-39.28571, -33.41261, 46.81889)

    controlPnt = np.array([pnt1, pnt2, pnt3])
    crv3d = nurbCurve(controlPnt, 2, 3)

    pnt = bezier3dCrv(crv3d, 0.1)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.2)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.3)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.4)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.5)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.6)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.7)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.8)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

    pnt = bezier3dCrv(crv3d, 0.9)
    print(pnt.x, ',', pnt.y, ',', pnt.z)
