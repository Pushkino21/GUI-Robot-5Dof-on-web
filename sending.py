#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:22:48 2024

@author: pushkinomikele
"""

from time import sleep

from smbus import SMBus
addr = 0x8
bus = SMBus(1)

def mapping(x, in_min, in_max, out_min, out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)
def ang(q1,q2,q3,q4,q5,q6):
    th1 = mapping(q1,-90,90,0,180)
    th2 = mapping(q2,-90,90,0,180)
    th3 = mapping(q3,-90,90,0,180)
    th4 = mapping(q4,-90,90,0,180)
    th5 = mapping(q5,-90,90,0,180)
    th6 = mapping(q6,-90,90,0,180)
    
    return [th1,th2,th3,th4,th5,th6]

def sent(q1,q2,q3,q4,q5,p):
    angulos = [0,0,0,0,0,40]
    angulos[0] = mapping(int(q1),-90,90,0,180)
    angulos[1] = mapping(int(q2),-90,90,0,180)
    angulos[2] = mapping(int(q3),-90,90,0,180)
    angulos[3] = mapping(int(q4),-90,90,0,180)
    angulos[4] = mapping(int(q5),-90,90,0,180)
    angulos[5] = mapping(int(p),-90,90,0,180)
    #print('sent')
    return bus.write_i2c_block_data(addr, 42,angulos)



