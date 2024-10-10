#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 19:24:34 2024

@author: pushkino
"""

import numpy as np
import plotly.express as px
import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
def mapping(x, in_min, in_max, out_min, out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

def directa(Q1,Q2,Q3,Q4,Q5):   
    q1 = np.deg2rad(Q1)
    q2 = np.deg2rad(Q2)
    q3 = np.deg2rad(Q3)
    q4 = np.deg2rad(Q4)
    q5 = np.deg2rad(Q5)
    
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

    A3 = np.array([[np.sin(q4), 0,  np.cos(q4), 0],
                   [-np.cos(q4), 0, np.sin(q4), 0],
                   [      0, -1,        0, 0],
                   [      0, 0,        0, 1]])

    A4 = np.array([[np.cos(q5), -np.sin(q5), 0, 0],
                   [np.sin(q5),  np.cos(q5), 0, 0],
                   [      0,        0, 1, 6.5],
                   [      0,        0, 0, 1]])



    #Coordenadas de la base
    #      x   y   z
    p0 = np.array([[0],[0],[0]])

    #Coordenadas de la hombro
    #      x   y   z
    p1 = [A0[(0,3)],A0[(1,3)],A0[(2,3)]]

    #Coordenadas codo
    A01 = np.dot(A0,A1)
    p2 = [A01[(0,3)],A01[(1,3)],A01[(2,3)]]

    #Coordenadas brazo
    A02 = np.dot(A01,A2)
    p3 = [A02[(0,3)],A02[(1,3)],A02[(2,3)]]

    #Coordenadas muñeca 1
    A03 = np.dot(A02,A3)
    p4 = [A03[(0,3)],A03[(1,3)],A03[(2,3)]]

    #Coordenadas codo
    A04 = np.dot(A03,A4)
    p5 = [A04[(0,3)],A04[(1,3)],A04[(2,3)]]

    #Matriz Rotacion
    rot = A04[0:3,0:3]

    #Coordenadas Ancho Pinza
    pi_iz = np.array([[0],[1],[0]])
    pi_de = np.array([[0],[-1],[0]])

    tpi_iz = np.dot(rot,pi_iz)
    tpi_de = np.dot(rot,pi_de)

    x5,y5,z5 = p5
    
    xiz,yiz,ziz = tpi_iz
    xde,yde,zde = tpi_de

    dxiz = float(x5+xiz)
    dyiz = float(y5+yiz)
    dziz = float(z5+ziz)

    dxde = float(x5+xde)
    dyde = float(y5+yde)
    dzde = float(z5+zde)
    
    #Coordenadas largo pinza
    l = np.array([[0],[0],[4]])
    lt = np.dot(rot,l)
    xlp,ylp,zlp = lt
    
    dxli = float(dxiz+xlp)
    dyli = float(dyiz+ylp)
    dzli = float(dziz+zlp)
    
    dxld = float(dxde+xlp)
    dyld = float(dyde+ylp)
    dzld = float(dzde+zlp)
    
    #pio.renderers.default = "browser"
    dots = [[0,p1[0],p2[0],p3[0],p4[0],p5[0],dxde,dxli,dxiz,dxld],
            [0,p1[1],p2[1],p3[1],p4[1],p5[1],dyde,dyli,dyiz,dyld],
            [0,p1[2],p2[2],p3[2],p4[2],p5[2],dzde,dzli,dziz,dzld]]
    #dots = {'x':[0],'y':[0],'z':[0]}
    # df = pd.DataFrame(data = dots)
    # fig = go.Figure()
    # fig.add_trace(go.Scatter3d(x=df['x'],
    #                            y=df['y'],
    #                            z=df['z'],
    #                            mode='lines+markers',
    #                            marker=dict(size=5, color="#fecea8"),
    #                            line=dict(width=8, color="#99b898")))
    
    # fig.update_layout(
    #     width=600,
    #     height=600,
    #     autosize=False,
    #     margin=dict(t=0, b=0, l=0, r=0),
    #     template="plotly_dark",
    #     scene = dict(
    #     xaxis = dict(nticks=15, range=[-27,27],),
    #                  yaxis = dict(nticks=15, range=[-27,27],),
    #                  zaxis = dict(nticks=15, range=[-10,38],),))
    #fig.update_traces(marker_size = 5, marker_color="#fecea8", line=dict(width=8,color="#99b898"))
    #pio.write_html(fig,"/home/pushkino/Escritorio/raspberrydownload/static/fig1.html")
    #print("ploteado")
    return dots #pio.show(fig)


def coordenadas(Q1,Q2,Q3,Q4,Q5):
    q1 = np.deg2rad(Q1)
    q2 = np.deg2rad(Q2)
    q3 = np.deg2rad(Q3)
    q4 = np.deg2rad(Q4)
    q5 = np.deg2rad(Q5)
    
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

    A3 = np.array([[np.sin(q4), 0,  np.cos(q4), 0],
                   [-np.cos(q4), 0, np.sin(q4), 0],
                   [      0, -1,        0, 0],
                   [      0, 0,        0, 1]])

    A4 = np.array([[np.cos(q5), -np.sin(q5), 0, 0],
                   [np.sin(q5),  np.cos(q5), 0, 0],
                   [      0,        0, 1, 6.5],
                   [      0,        0, 0, 1]])





    #Coordenadas de la base
    #      x   y   z
    p0 = np.array([[0],[0],[0]])

    #Coordenadas de la hombro
    #      x   y   z
    p1 = [A0[(0,3)],A0[(1,3)],A0[(2,3)]]

    #Coordenadas codo
    A01 = np.dot(A0,A1)
    p2 = [A01[(0,3)],A01[(1,3)],A01[(2,3)]]

    #Coordenadas brazo
    A02 = np.dot(A01,A2)
    p3 = [A02[(0,3)],A02[(1,3)],A02[(2,3)]]

    #Coordenadas muñeca 1
    A03 = np.dot(A02,A3)
    p4 = [A03[(0,3)],A03[(1,3)],A03[(2,3)]]

    #Coordenadas codo
    A04 = np.dot(A03,A4)
    p5 = [A04[(0,3)],A04[(1,3)],A04[(2,3)]]

    #Matriz Rotacion
    rot = A04[0:3,0:3]

    #Coordenadas Ancho Pinza
    pi_iz = np.array([[0],[1],[0]])
    pi_de = np.array([[0],[-1],[0]])

    tpi_iz = np.dot(rot,pi_iz)
    tpi_de = np.dot(rot,pi_de)

    x5,y5,z5 = p5

    return [x5,y5,z5]

def euler(Q1,Q2,Q3,Q4,Q5):
    q1 = np.deg2rad(Q1)
    q2 = np.deg2rad(Q2)
    q3 = np.deg2rad(Q3)
    q4 = np.deg2rad(Q4)
    q5 = np.deg2rad(Q5)
    
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

    A3 = np.array([[np.sin(q4), 0,  np.cos(q4), 0],
                   [-np.cos(q4), 0, np.sin(q4), 0],
                   [      0, -1,        0, 0],
                   [      0, 0,        0, 1]])

    A4 = np.array([[np.cos(q5), -np.sin(q5), 0, 0],
                   [np.sin(q5),  np.cos(q5), 0, 0],
                   [      0,        0, 1, 6.5],
                   [      0,        0, 0, 1]])




    #Coordenadas de la base
    #      x   y   z
    p0 = np.array([[0],[0],[0]])

    #Coordenadas de la hombro
    #      x   y   z
    p1 = [A0[(0,3)],A0[(1,3)],A0[(2,3)]]

    #Coordenadas codo
    A01 = np.dot(A0,A1)
    p2 = [A01[(0,3)],A01[(1,3)],A01[(2,3)]]

    #Coordenadas brazo
    A02 = np.dot(A01,A2)
    p3 = [A02[(0,3)],A02[(1,3)],A02[(2,3)]]

    #Coordenadas muñeca 1
    A03 = np.dot(A02,A3)
    p4 = [A03[(0,3)],A03[(1,3)],A03[(2,3)]]

    #Coordenadas codo
    A04 = np.dot(A03,A4)
    p5 = [A04[(0,3)],A04[(1,3)],A04[(2,3)]]
    #print(A04)
    #Matriz Rotacion
    rot = A04[0:3,0:3]
    r21 = rot[(1,0)]
    r11 = rot[(0,0)]
    r31 = rot[(2,0)]
    r32 = rot[(2,1)]
    r33 = rot[(2,2)]
    r22 = rot[(1,1)]
    r12 = rot[(0,1)]
    r23 = rot[(1,2)]
    r13 = rot[(0,2)]
    
    #print(rot)
    # if r11==r21==0:
    #     alpha = 0
    #     beta = np.pi/2
    #     gamma = np.arctan(r12/r22)
        
    # else:
    #     alpha = np.arctan2(r21,r11)
    #     beta = np.arctan2(-r31,np.sqrt((r11**2)+(r21**2)))
    #     gamma = np.arctan(r32/r33)
    alpha = np.arctan2(r23,r13)
    beta = np.arctan2(np.sqrt(1-(r33**2)),r33)
    gamma = np.arctan2(r32,-r31)
    
    return np.rad2deg([alpha,beta,gamma])