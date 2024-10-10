#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:01:28 2024

@author: pushkino
"""
import numpy as np
from Directa import directa
def inversa (x,y,z,a,b,g):
    #····································#
    #       Calculos para Inversa        #
    #····································#
    alpha= np.deg2rad(a)
    beta = np.deg2rad(b)
    gamma = np.deg2rad(g)
    #Constantes del robot (eslabones)

    l1 = 10
    l2 = 10
    l3 = 9.5

    ze = np.array([[np.cos(alpha), -np.sin(alpha), 0],
                   [np.sin(alpha), np.cos(alpha), 0],
                   [0, 0, 1]])

    ye = np.array([[np.cos(beta), 0 ,np.sin(beta)],
                   [0, 1,0],
                   [-np.sin(beta),0,np.cos(beta)]])
    
    # zf = np.array([[1,0,0],
    #                 [0, np.cos(gamma), -np.sin(gamma)],
    #                 [0, np.sin(gamma), np.cos(gamma)]])
    
    zf = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                  [np.sin(gamma), np.cos(gamma), 0],
                  [0, 0, 1]])
    t = np.dot(ze,ye)
    rt = np.dot(t,zf)

    # Centro de la muñeca

    P = np.array([[x],
                  [y],
                  [z]])

    tcp = np.array([[0],
                    [0],
                    [6.5]])

    tvector = np.dot(rt,tcp)

    c_wrist = P-tvector

    pmx,pmy,pmz = c_wrist

    # Calculo de catetos e hipotenusa tringulos etc

    r3 = pmz-l1
    r1 = np.sqrt((pmx**2)+(pmy**2)+(r3**2))
    r2 = np.sqrt((pmx**2)+(pmy**2))

    #Calculo de q1

    q1 = float(np.arctan2(pmy,pmx))
    
    #print("Valor q1: ",np.rad2deg(q1))
    #print('pmz = ',pmz)

    #Calculo q2
    #Angulo Beta
    cobet = ((l2**2)+(r1**2)-(l3**2))/(2*l2*r1)
    sibet = np.sqrt(1-(cobet**2))


    try:
        bet = np.arctan(sibet/cobet)
        #print('beta = ',np.rad2deg(bet))
    except Exception:
        print("error")
        
    gam = np.arctan(r2/r3)
    #print('gam = ',np.rad2deg(gam))
    #q2 = float(bet+gam)

    if z <4:
        #print('Seno beta',np.rad2deg(sibet))
        #print('Cos beta',np.rad2deg(cobet))
        gam = np.arctan(-r2/r3)
        #print('Segundo gam: ',gam)
        q2 = float(bet - gam)
        #print("Valor q2: ",np.rad2deg(q2)," caso1")
    else:
        q2 = float(bet - gam)
        #print("Valor q2: ",np.rad2deg(q2)," caso2")
        
    #Calculo de Q3
    phi =(np.pi/2)-bet;

    coalp = ((r1**2)+(l3**2)-(l2**2))/(2*r1*l3)
    sialp = np.sqrt(1-(coalp**2))

    alph = np.arctan(sialp/coalp)

    q3 = float(alph-phi)
    #print("Valor q3: ",np.rad2deg(q3))

    #Calculo de q4 y q5

    A0 = np.array([[np.cos(q1), 0,  np.sin(q1),  0],
               [np.sin(q1), 0, -np.cos(q1),  0],
               [      0, 1,        0, 10],
               [      0, 0,        0,  1]])

    A1 = np.array([[-np.sin(q2),  np.cos(q2),  0, -10*np.sin(q2)],
               [np.cos(q2), np.sin(q2),  0, 10*np.cos(q2)],
               [      0,        0, -1,          0],
               [      0,        0,  0,          1]])

    A2 = np.array([[-np.sin(q3),  np.cos(q3),  0, -9.5*np.sin(q3)],
               [np.cos(q3), np.sin(q3),  0, 9.5*np.cos(q3)],
               [      0,        0, -1,          0],
               [      0,        0,  0,          1]])

    A01 = np.dot(A0,A1)
    A02 = np.dot(A01,A2)

    rot = A02[0:3,0:3]

    #rot_inv = np.linalg.inv(rot)
    rot_inv = np.transpose(rot)
    rf = np.dot(rot_inv,rt)
    #print(rf)
    q4 = np.arctan(rf[(1,2)]/rf[(0,2)])
    #q4 = (dof4-0)*(-(np.pi/2)-(np.pi/2))/(np.pi-0)+(np.pi/2)
    # q55 = np.arctan2(rf[(2,0)],rf[(2,1)])
    # if q55 == np.pi:
    #     q5 = 0
    # else:
    #     q5 = q55
    q5 = np.arctan(rf[(2,0)]/rf[(2,1)])
    return [q1,q2,q3,q4,q5]
