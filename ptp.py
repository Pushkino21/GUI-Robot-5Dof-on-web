#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:41:11 2024

@author: pushkino
"""

import numpy as np
import matplotlib.pyplot as plt
def A(inicio,final,tini,tfin):
    t0 = tini
    tf = tfin
    q0 = inicio
    q_0 = 0
    q__0 = 0

    qf = final
    q_f = 0
    q__f = 0

    time_mat = np.array([[1,t0,t0**2,t0**3,t0**4,t0**5],
                  [0,1,2*t0,3*t0**2,4*t0**3,5*t0**4],
                  [0,0,2,6*t0,12*t0**2,20*t0**3],
                  [1,tf,tf**2,tf**3,tf**4,tf**5],
                  [0,1,2*tf,3*tf**2,4*tf**3,5*tf**4],
                  [0,0,2,6*tf,12*tf**2,20*tf**3]])

    time_inv = np.linalg.inv(time_mat)

    res = np.array([[q0],
                    [q_0],
                    [q__0],
                    [qf],
                    [q_f],
                    [q__f]])

    a = np.dot(time_inv,res)
    return a
def pos (a0,a1,a2,a3,a4,a5,t):
    Q = (a0)+(a1*t)+(a2*t**2)+(a3*t**3)+(a4*t**4)+(a5*t**5)
    return Q
def vel(a0,a1,a2,a3,a4,a5,t):
    return
def acc(a0,a1,a2,a3,a4,a5,t):
    return
# t0 = 0
# tf = 1
# qini = 0
# qfin = 90
# paso = 50
# time = np.linspace(t0, tf,num=paso)
# values = []
# pp = []
# a = A(qini,qfin,t0,tf)

# for i in range(paso):
#     Q = pos(a[0],a[1],a[2],a[3],a[4],a[5],time[i])
#     values.append(Q)
    
# val = np.array(values)
# for i in range(paso):
#     p = int(values[i])
#     pp.append(p)

# print(pp)
# plt.plot(time,val)
# plt.grid('on')
# plt.show()