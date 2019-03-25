#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 21:18
# @Author  : Lens
# @Version : 3.7
# @File    : arcIsLine.py
# @Software: PyCharm


import numpy as np


def arcIsLine(startDeg, endDeg):

    startRad = np.deg2rad(startDeg)
    endRad = np.deg2rad(endDeg)

    theta = np.fabs(endDeg - startDeg)

    if np.fabs(np.sin(theta) - theta) < 1.0e-9:
        return True
    else:
        return False


if __name__ == "__main__":
    arcIsLine(0, 0.008159831)


