#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/24/2019 3:41 PM
# @Author  : Lens
# @Version : 3.7
# @File    : bezierSurf.py
# @Software: PyCharm

import numpy as np
from surf.surfInfo import nurbSurf, point, nurbCurve
from curve.bezier3dCrv import bezier3dCrv

def bezierSurf(srf, ut, vt):

    u = srf.udegree
    v = srf.vdegree
    cp = srf.cp
    dim = srf.dim
    type = srf.type

    pntLst = np.array([])
    if srf.dim != 3:
        return None

    if u+1 != cp.shape[0]:
        return None

    if v+1 != cp.shape[1]:
        return None

    for eachCrvCp in cp:
        crv3d = nurbCurve(eachCrvCp, u, dim)
        pnt = bezier3dCrv(crv3d, ut)

        pntLst = np.append(pntLst, pnt)

    crv3d = nurbCurve(pntLst, v, dim)
    pnt = bezier3dCrv(crv3d, ut)

    return pnt

if __name__ == "__main__":

    pnt1 = point(-65.16052, 41.26041, 0)
    pnt2 = point(-113.6742, 13.91201, 0)
    pnt3 = point(-61.11772, -33.41261, 0)
    pntLst1 = np.array([pnt1, pnt2, pnt3])

    pnt1 = point(-65.16052, 41.26041, 30.38485)
    pnt2 = point(-113.6742, 13.91201, 53.00715)
    pnt3 = point(-61.11772, -33.41261, 28.49966)
    pntLst2 = np.array([pnt1, pnt2, pnt3])

    pnt1 = point(-41.88438, 41.26041, 49.91586)
    pnt2 = point(-73.06837, 13.91201, 87.07949)
    pnt3 = point(-39.28571, -33.41261, 46.81889)
    pntLst3 = np.array([pnt1, pnt2, pnt3])

    pntLst = np.array([pntLst1, pntLst2, pntLst3])
    srf = nurbSurf(pntLst, 2, 2, 3)

    pnt = bezierSurf(srf, 0.5, 0.5)
    print(pnt.x, ',', pnt.y, ',', pnt.z)

