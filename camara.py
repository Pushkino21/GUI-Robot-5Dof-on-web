#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 00:27:05 2024

@author: pushkinomikele
"""

import numpy as np
import cv2

cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.resizeWindow('thresh', 400, 680)
 
cap = cv2.VideoCapture(0,cv2.CAP_V4L2)

while True:
    # Read from camera
    source, frame = cap.read()
     
    if not source:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Original',frame)

#cap.release()
cv2.destroyAllWindows()