#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/30 15:04
# @Author  : Lens
# @Site    : 
# @File    : bestFitEllipse.py
# @Software: PyCharm

import numpy as np

def least_error_solve(g, iteratePnt, fittingPnt):
    a = g[0]
    b = g[1]
    xc = g[2]
    yc = g[3]
    theta = g[4]
    x = iteratePnt[0]
    y = iteratePnt[1]
    xi = fittingPnt[0]
    yi = fittingPnt[1]

    q = create_Q_matrix(g, iteratePnt, fittingPnt)
    f00 = 0.5*(a*a*y*y + b*b*x*x - a*a*b*b)
    f10 = b*b*x*(yi - y) - a*a*y*(xi - x)

    f = np.array([f00,f10]).transpose()

    invq = np.linalg.inv(q)
    deltaPnt = invq.dot(f)
    deltaPnt = deltaPnt.transpose()
    return deltaPnt


def create_Q_matrix(g,pntInter, pnt):
    a = g[0]
    b = g[1]
    xc = g[2]
    yc = g[3]
    theta = g[4]

    x = pntInter[0]
    y = pntInter[1]
    xi = pnt[0]
    yi = pnt[1]

    q00 = b * b * x
    q01 = a * a * y
    q10 = (a * a - b * b) * y + b * b * yi
    q11 = (a * a - b * b) * x - a * a * xi
    q = np.array([[q00, q01], [q10, q11]])
    return q

def least_error_newton(g, iteratePnt, fittingPnt):

    deltaPnt = least_error_solve(g, iteratePnt, fittingPnt)

    intersectPnt = iteratePnt

    while (np.fabs(deltaPnt) > 1.0e-12).any():
        intersectPnt = intersectPnt - deltaPnt
        deltaPnt = least_error_solve(g, intersectPnt, fittingPnt)

    return intersectPnt

def transform_new_coordinate(g, pntLst):
    a = g[0]
    b = g[1]
    xc = g[2]
    yc = g[3]
    theta = g[4]

    new_pntLst = np.array([])

    R = create_R_matrix(g)
    for pnt in pntLst:
        new_pnt = R.dot(np.array([[pnt[0] - xc],[pnt[1] - yc]]))
        new_pntLst = np.append(new_pntLst, new_pnt)

    row_n = np.size(new_pntLst) / 2
    return new_pntLst.reshape(row_n, 2)

def transform_old_coordinate(g, pntLst):
    a = g[0]
    b = g[1]
    xc = g[2]
    yc = g[3]
    theta = g[4]

    new_pntLst = np.array([])

    origin = np.array([xc, yc]).transpose()

    R = create_R_matrix(g)
    R = R.transpose()

    for pnt in pntLst:
        new_pnt = R.dot(pnt.transpose()) + origin
        new_pntLst = np.append(new_pntLst, new_pnt)

    row_n = np.size(new_pntLst) / 2
    return new_pntLst.reshape(row_n, 2)


def create_R_matrix(g):
    theta = g[4]
    R = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    return R


def square_error_min(g, pntLst):
    a = g[0]
    b = g[1]
    xc = g[2]
    yc = g[3]
    theta = g[4]

    delta_dist = np.array([])
    new_pntLst = transform_new_coordinate(g, pntLst)
    jacobi = np.array([[]])
    jacobi.resize(0,5)
    for pnt in new_pntLst:
        xi1 = pnt[0]
        yi1 = pnt[1]
        const_num = np.sqrt(b*b*xi1*xi1 + a*a*yi1*yi1)
        const_num = a*b/const_num
        xk1 = pnt*const_num

        xk2 = np.array([])
        if np.fabs(xi1) < a:
            xi2 = xi1
            yi2 = np.sign(yi1)*b/a*np.sqrt(a*a - xi1*xi1)
            xk2 = np.append(xk2,[xi2, yi2])
        else:
            xi2 = np.sign(xi1)*a
            yi2 = 0
            xk2 = np.append(xk2,[xi2, yi2])

        x_it = 0.5*(xk1 + xk2)
        min_dist_pnt = least_error_newton(g, x_it, pnt)

        jacobi_xi = create_jacobi_matrix(g, min_dist_pnt, pnt)
        n,_ = jacobi.shape

        jacobi = np.insert(jacobi, n, jacobi_xi, 0)

        delta_dist = np.append(delta_dist, min_dist_pnt)

    row_n = np.size(delta_dist) / 2
    delta_dist = delta_dist.reshape(row_n, 2)
    old_intersect = transform_old_coordinate(g, delta_dist)

    min_dist_error = pntLst - old_intersect
    min_dist_error = min_dist_error.reshape(min_dist_error.size, 1)
    return min_dist_error[:,0], jacobi

def create_jacobi_matrix(g, pntInter, pnt):
    a = g[0]
    b = g[1]
    xc = g[2]
    yc = g[3]
    theta = g[4]
    x = pntInter[0]
    y = pntInter[1]
    xi = pnt[0]
    yi = pnt[1]

    Q = create_Q_matrix(g, pntInter, pnt)
    R = create_R_matrix(g)

    invR = R.transpose()
    invQ = np.linalg.inv(Q)

    b00 = b*b*x*np.cos(theta) - a*a*y*np.sin(theta)
    b10 = b*b*(yi - y)*np.cos(theta) + a*a*(xi - x)*np.sin(theta)

    B1 = np.array([b00, b10])

    b00 = b*b*x*np.sin(theta) + a*a*y*np.cos(theta)
    b10 = b*b*(yi - y)*np.sin(theta) - a*a*(xi - x)*np.cos(theta)
    B2 = np.array([b00, b10])

    b00 = a*(b*b - y*y)
    b10 = 2*a*y*(xi - x)
    B3 = np.array([b00, b10])

    b00 = b*(a*a - x*x)
    b10 = -2*b*x*(yi - y)
    B4 = np.array([b00, b10])

    b00 = (a*a - b*b)*x*y
    b10 = (a*a - b*b)*(x*x - y*y - x*xi +y*yi)
    B5 = np.array([b00, b10])

    B = np.array([B1, B2, B3, B4, B5])
    B = B.transpose()
    jacobi = invR.dot(invQ)
    jacobi = jacobi.dot(B)

    return jacobi

def least_sqaure_fit(g, pntLst):

    min_dist_error, jacobi = square_error_min(g, pntLst)

    # JacobiMat = np.dot(jacobi.transpose(), jacobi)

    u,d,v = np.linalg.svd(jacobi)

    # b = np.dot(jacobi.transpose(), min_dist_error)

    x1 = np.dot(np.linalg.inv(u), min_dist_error)

    diagMat = np.zeros((5, len(pntLst) * 2))
    for i in range(len(d)):
        if np.fabs(d[i]) > 1.0e-12:
            diagMat[i][i] = 1/d[i]

    x2 = np.dot(diagMat, x1)
    x3 = np.dot(np.linalg.inv(v), x2)
    solve_x = x3

    length = np.linalg.norm(solve_x, 2)
    while length > 1.0e-2:
        g[0] = g[0]+ solve_x[2]
        g[1] = g[1]+ solve_x[3]
        g[2] = g[2]+ solve_x[0]
        g[3] = g[3]+ solve_x[1]
        g[4] = g[4]+ solve_x[4]

        if g[0] < g[1]:
            g[0],g[1] = g[1],g[0]
            g[4] = g[4] - np.sign(g[4])*np.pi/2
        min_dist_error, jacobi = square_error_min(g, pntLst)

        # JacobiMat = np.dot(jacobi.transpose(), jacobi)

        u, d, v = np.linalg.svd(jacobi)

        # b = np.dot(jacobi.transpose(), min_dist_error)

        x1 = np.dot(np.linalg.inv(u), min_dist_error)

        diagMat = np.zeros((5, len(pntLst)*2))
        for i in range(len(d)):
            if np.fabs(d[i]) > 1.0e-12:
                diagMat[i][i] = 1 / d[i]

        x2 = np.dot(diagMat, x1)
        x3 = np.dot(np.linalg.inv(v), x2)
        solve_x = x3
        length = np.linalg.norm(solve_x, 2)
    return g

if __name__ == "__main__":
    # g = np.array([3.5204629269616410, 3.5204629269616410, 4.7487091222030990, 5.0068846815834780, 0])
    # pntLst = np.array([[1,7],[7,7],[9,5],[3,7],[6,2],[8,4]])
    # g = least_sqaure_fit(g, pntLst)
    # print(g)
    g = np.array([2.73266224 ,1.90678367, 6.07513577, 6.18004716,- 1.26908651])
    x_it =np.array([2.60078539, - 0.40865047])
    pnt = np.array([3.96890679, - 1.31385637])
    min_dist_pnt = least_error_newton(g, x_it, pnt)
