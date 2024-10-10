#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:51:43 2024

@author: pushkino
"""

from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO, send, emit
from Directa import directa, coordenadas, euler
from inverse import inversa
#from sending import sent
from ptp import A, pos
import numpy as np
from time import sleep
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)
app.secret_key = "lol"
app.config['SECRET_KEY']='lol'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/directa")
def d_ind():
    th1 = 0
    th2 = 0
    th3 = 0
    th4 = 0
    th5 = 0
    p = -60
    th1_value = th1
    th2_value = th2
    th3_value = th3
    th4_value = th4
    th5_value = th5
    pinza_value = p
    directa(th1, th2, th3, th4, th5)
    x,y,z = coordenadas(th1, th2, th3, th4, th5)
    x_value = x
    y_value = y
    z_value = z
    #sent(th1, th2, th3, th4, th5, p)
    a,b,g = euler(th1, th2, th3, th4, th5)
    return render_template("directa.html",th1_value=th1_value,
                           th2_value=th2_value,
                           th3_value=th3_value,
                           th4_value=th4_value,
                           th5_value=th5_value,
                           pinza_value=pinza_value, x_value=x_value, y_value=y_value, z_value=z_value, a_value=a,b_value=b, g_value=g)

@app.route("/inversa")
def inverse():
    x = 16
    y = 0
    z = 20
    a = 0
    b = 90
    g = 0
    p = -60
    x_value = x
    y_value = y
    z_value = z
    pinza_value=p
    coor = np.rad2deg(inversa(x, y, z, a, b, g))
    th1_value,th2_value,th3_value,th4_value,th5_value = np.round(coor)
    directa(th1_value, th2_value, th3_value, th4_value, th5_value)
    #sent(th1_value, th2_value, th3_value, th4_value, th5_value,p)
    return render_template("inversa.html",th1_value=th1_value,
                           th2_value=th2_value,
                           th3_value=th3_value,
                           th4_value=th4_value,
                           th5_value=th5_value,
                           pinza_value=pinza_value, x_value=x_value, y_value=y_value, z_value=z_value, a_value=a,b_value=b, g_value=g)

@app.route("/ptp")
def ptp():
    return render_template("ptp.html")


@app.route("/fk", methods=['POST'])
def fk():
    th1 = int(request.form["Q1"])
    th2 = int(request.form["Q2"])
    th3 = int(request.form["Q3"])
    th4 = int(request.form["Q4"])
    th5 = int(request.form["Q5"])
    p = int(request.form["PINZA"])
    th1_value = th1
    th2_value = th2
    th3_value = th3
    th4_value = th4
    th5_value = th5
    pinza_value = p
    fig = directa(th1, th2, th3, th4, th5)
    graph_html = pio.to_html(fig, full_html=False)
    emit('update_plot',graph_html)
    x,y,z = coordenadas(th1, th2, th3, th4, th5)
    x_value = x
    y_value = y
    z_value = z
    #sent(th1, th2, th3, th4, th5, p)
    a,b,g = euler(th1, th2, th3, th4, th5)
    return render_template("directa.html",th1_value=th1_value,
                           th2_value=th2_value,
                           th3_value=th3_value,
                           th4_value=th4_value,
                           th5_value=th5_value,
                           pinza_value=pinza_value, x_value=x_value, y_value=y_value, z_value=z_value, a_value=a,b_value=b, g_value=g)
@socketio.on('fork')
def fk(msg):
    q1,q2,q3,q4,q5,p = msg
    Q1 = int(q1)
    Q2 = int(q2)
    Q3 = int(q3)
    Q4 = int(q4)
    Q5 = int(q5)
    data = directa(Q1,Q2,Q3,Q4,Q5)
    x,y,z = data
    emit('data',{'x':x,'y':y,'z':z})
    # graph_html = pio.to_html(fig, full_html=False)
    # emit('update_plot',graph_html)
    #sleep(.10)

    xyz = coordenadas(Q1,Q2,Q3,Q4,Q5)
    emit('coor',xyz)
    a,b,c = euler(Q1,Q2,Q3,Q4,Q5)
    abc=[a,b,c]
    #print(xyz)
    emit('eu',abc)
    #sent(q1, q2, q3, q4, q5, p)

    print("Calculada Directa")

@socketio.on('ptp')
def peer2peer(ang):
    print(ang)
    inicial,final = ang
    pf,q5f,q4f,q3f,q2f,q1f = final
    p,q5,q4,q3,q2,q1 = inicial
    th1 = float(q1)
    th2 = float(q2)
    th3 = float(q3)
    th4 = float(q4)
    th5 = float(q5)
    p = float(p)
    
    q1f = float(q1)
    q2f = float(q2)
    q3f = float(q3)
    q4f = float(q4)
    q5f = float(q5)
    pf = float(pf)
    
    q1 = th1
    q2 = th2
    q3 = th3
    q4 = th4
    q5 = th5

    """PTP implementation"""
    ti = 0
    tf = 2
    paso = 50
    time = np.linspace(ti, tf,paso)
    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    Q5 = []
    P = []
    
    q1_values = []
    q2_values = []
    q3_values = []
    q4_values = []
    q5_values = []
    pn_values = []
    
    aq1 = A(q1, q1f, ti, tf)
    aq2 = A(q2, q2f, ti, tf)
    aq3 = A(q3, q3f, ti, tf)
    aq4 = A(q4, q4f, ti, tf)
    aq5 = A(q5, q5f, ti, tf)
    pna = A(p, pf, ti, tf)
    
    for i in range(paso):
        q1v = pos(aq1[0],aq1[1],aq1[2],aq1[3],aq1[4],aq1[5],time[i])
        q1_values.append(q1v)
        q2v = pos(aq2[0],aq2[1],aq2[2],aq2[3],aq2[4],aq2[5],time[i])
        q2_values.append(q2v)
        q3v = pos(aq3[0],aq3[1],aq3[2],aq3[3],aq3[4],aq3[5],time[i])
        q3_values.append(q3v)
        q4v = pos(aq4[0],aq4[1],aq4[2],aq4[3],aq4[4],aq4[5],time[i])
        q4_values.append(q4v)
        q5v = pos(aq5[0],aq5[1],aq5[2],aq5[3],aq5[4],aq5[5],time[i])
        q5_values.append(q5v)
        pnv = pos(pna[0],pna[1],pna[2],pna[3],pna[4],pna[5],time[i])
        pn_values.append(pnv)
    for j in range(paso):
        pq1 = int(q1_values[j])
        Q1.append(pq1)
        pq2 = int(q2_values[j])
        Q2.append(pq2)
        pq3 = int(q3_values[j])
        Q3.append(pq3)
        pq4 = int(q4_values[j])
        Q4.append(pq4)
        pq5 = int(q5_values[j])
        Q5.append(pq5)
        pqp = int(pn_values[j])
        P.append(pqp)
    for k in range(paso):
        #sent(Q1[k],Q2[k],Q3[k],Q4[k],Q5[k],P[k])
        #data = directa(Q1[k],Q2[k],Q3[k],Q4[k],Q5[k])
        #x,y,z = data
        
        #emit('data',{'x':x,'y':y,'z':z})
        # graph_html = pio.to_html(fig, full_html=False)
        # emit('update_plot',graph_html)
        #sleep(.10)
        pass
        """PTP end"""

@socketio.on('invk')
#@app.route("/ik",methods=['POST'])
def ik (msg):
    print(msg)
    xh,yh,zh,ah,bh,gh,ph=msg
    print(ph)
    x = float(xh)
    y = float(yh)
    z = float(zh)
    a = float(ah)
    b = float(bh)
    g = float(gh)
    p = int(ph)
    # x_value = x
    # y_value = y
    # z_value = z
    # pinza_value=p
    
    angulos = np.rad2deg(inversa(x, y, z, a, b, g))
    th1,th2,th3,th4,th5 = np.round(angulos)
    theta = [th1,th2,th3,th4,th5]
    emit('ang',theta)
    
    data = directa(th1,th2,th3,th4,th5)
    x,y,z = data
    emit('data',{'x':x,'y':y,'z':z})
    # fig = directa(th1, th2, th3, th4, th5)
    # graph_html = pio.to_html(fig, full_html=False)
    # emit('update_plot',graph_html)
    #sent(th1, th2, th3, th4, th5,p)
    print("inversa calculada")
    

@app.route("/peer", methods=['POST'])
def peer():
    q1 = int(request.form["Q1"])
    q2 = int(request.form["Q2"])
    q3 = int(request.form["Q3"])
    q4 = int(request.form["Q4"])
    q5 = int(request.form["Q5"])
    p = int(request.form["PINZA"])
    
    q1f = int(request.form["Q1f"])
    q2f = int(request.form["Q2f"])
    q3f = int(request.form["Q3f"])
    q4f = int(request.form["Q4f"])
    q5f = int(request.form["Q5f"])
    pf = int(request.form["PINZAf"])
    
    ti = 0
    tf = 2
    paso = 50
    time = np.linspace(ti, tf,paso)
    
    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    Q5 = []
    P = []
    
    q1_values = []
    q2_values = []
    q3_values = []
    q4_values = []
    q5_values = []
    pn_values = []
    
    aq1 = A(q1, q1f, ti, tf)
    aq2 = A(q2, q2f, ti, tf)
    aq3 = A(q3, q3f, ti, tf)
    aq4 = A(q4, q4f, ti, tf)
    aq5 = A(q5, q5f, ti, tf)
    pna = A(p, pf, ti, tf)
    
    for i in range(paso):
        q1v = pos(aq1[0],aq1[1],aq1[2],aq1[3],aq1[4],aq1[5],time[i])
        q1_values.append(q1v)
        q2v = pos(aq2[0],aq2[1],aq2[2],aq2[3],aq2[4],aq2[5],time[i])
        q2_values.append(q2v)
        q3v = pos(aq3[0],aq3[1],aq3[2],aq3[3],aq3[4],aq3[5],time[i])
        q3_values.append(q3v)
        q4v = pos(aq4[0],aq4[1],aq4[2],aq4[3],aq4[4],aq4[5],time[i])
        q4_values.append(q4v)
        q5v = pos(aq5[0],aq5[1],aq5[2],aq5[3],aq5[4],aq5[5],time[i])
        q5_values.append(q5v)
        pnv = pos(pna[0],pna[1],pna[2],pna[3],pna[4],pna[5],time[i])
        pn_values.append(pnv)
    for j in range(paso):
        pq1 = int(q1_values[j])
        Q1.append(pq1)
        pq2 = int(q2_values[j])
        Q2.append(pq2)
        pq3 = int(q3_values[j])
        Q3.append(pq3)
        pq4 = int(q4_values[j])
        Q4.append(pq4)
        pq5 = int(q5_values[j])
        Q5.append(pq5)
        pqp = int(pn_values[j])
        P.append(pqp)
    for k in range(paso):
        #sent(Q1[k],Q2[k],Q3[k],Q4[k],Q5[k],P[k])
        sleep(tf/paso)
    directa(Q1[49],Q2[49],Q3[49],Q4[49],Q5[49])
    return render_template("ptp.html",th1_value=q1,
                           th2_value=q2,
                           th3_value=q3,
                           th4_value=q4,
                           th5_value=q5,
                           pinza_value=p,
                           th1f_value=q1f,
                           th2f_value=q2f,
                        th3f_value=q3f,
                        th4f_value=q4f,
                        th5f_value=q5f,
                        pinzaf_value=pf)


if __name__ == '__main__':
     socketio.run(app)
