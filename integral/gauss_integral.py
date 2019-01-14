#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/14 21:00
# @Author  : Lens
# @Version : 3.7
# @File    : gauss_integral.py
# @Software: PyCharm


import numpy as np


def gauss_integral_coefficient(n):

    xi = np.array([])
    ci = np.array([])

    if n == 2:
        x1 = np.sqrt(1.0/3)

        xi = np.append(xi, [-x1, x1])
        ci = np.append(ci, [1.0, 1.0])

    elif n == 3:
        x1 = np.sqrt(3.0/5)

        y1 = 5.0/9
        y2 = 8.0/9

        xi = np.append(xi, [-x1, 0, x1])
        ci = np.append(ci, [y1, y2, y1])

    elif n == 4:
        x1 = np.sqrt((15 + 2 * np.sqrt(30)) / 35)
        x2 = np.sqrt((15 - 2 * np.sqrt(30)) / 35)

        y1 = (90 - 5 * np.sqrt(30)) / 180
        y2 = (90 + 5 * np.sqrt(30)) / 180

        xi = np.append(xi, [-x1, -x2, x2, x1])
        ci = np.append(ci, [y1, y2, y2, y1])

    return xi, ci


def gauss_integral(a,b,integralFunc, n):

    xi, ci = gauss_integral_coefficient(n)

    integral = 0.0

    for i in range(n):
        x = ((b-a) * xi [i] + b + a) / 2
        integral +=  ci[i] * integralFunc(x) * (b-a) / 2.0

    return integral

def integralFunc(x):
    return np.log(x) / np.log(np.e)

def integralFunc1(x):
    return np.exp(-x*x / 2.0)

if __name__ == "__main__":
    i = gauss_integral(-1,1, integralFunc1, 3)
    print(i)
