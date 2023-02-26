#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:56:30 2021

@author: anandarupmukherjee
"""

import re
import numpy as np
# import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from scipy.signal import blackman
from scipy.fft import fft
from sklearn.cluster import KMeans
from scipy.signal import find_peaks




import socket 
import time
import re
import os
from datetime import date
from datetime import datetime
import serial
import csv
import psutil
import pickle
import numpy as np
from scipy.fft import fft
# import matplotlib.pyplot as plt


################## FUNCTIONS ###################
def freq_analysis_dataset(p1,p2,p3):
    # Number of sample points
    N = 50
    # sample spacing
    T = 1.0 / 100.0
    w = blackman(N)
    arr_x=[]
    arr_y=[]
    arr_z=[]
    arr_xp=[]
    arr_yp=[]
    arr_zp=[]
    lmt = round(len(p1)/N)                          #change here
    
    for i in range(1,lmt-1):
        yx = p1[i*N:(i+1)*N]                          #change here
        yy = p2[i*N:(i+1)*N]
        yz = p3[i*N:(i+1)*N]
    
        yfx = fft(yx*w)
        yfy = fft(yy*w)
        yfz = fft(yz*w)
        
        peaksX, _ = find_peaks(yfx, height=0)
        peaksY, _ = find_peaks(yfy, height=0)
        peaksZ, _ = find_peaks(yfz, height=0)
        
        arr_x.append(yfx)
        arr_y.append(yfy)
        arr_z.append(yfz)
        
        arr_xp.append(peaksX)
        arr_yp.append(peaksY)
        arr_zp.append(peaksZ)
    
    #anand's sensor fusion equation (have to check goodness)
    # t_var= np.sqrt(np.array(arr_x)**2 + np.array(arr_y)**2 + np.array(arr_z)**2)
    t_var= np.sqrt(np.array(arr_x)**2 + np.array(arr_y)**2 + np.array(arr_z)**2)
    return abs(t_var)

def DashInsert(text):
    list_int = map(int, list(text))
    list_str = map(str, list_int)
    return list_str



count_main=-1
count_a=0
count_b=0


filename = 'DMW_learner.sav'
loaded_model = pickle.load(open(filename, 'rb'))
X=[]



# ser_v = serial.Serial('/dev/cu.usbserial-0001', 115200)
# ser_v.flushInput()
# ser_v.flushOutput()

UDP_IP = "10.0.0.5" 
UDP_PORT = 9001

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


datx=[]
i=0

while True:
    # ser_v_bytes = ser_v.readline()
    ser_v_bytes,addr=sock.recvfrom(1024)
    # print(ser_v_bytes)
    dec1=ser_v_bytes.decode("utf-8").split('A')[1]
    dec2=dec1.split('C')[0]
    gx=dec2.split(',')[0] # put string split again wrt comma
    gy=dec2.split(',')[1]
    gz=dec2.split(',')[2]
    ax=dec2.split(',')[3]
    ay=dec2.split(',')[4]
    az=dec2.split(',')[5]
    X=[float(ax),float(ay),float(az), float(gx),float(gy),float(gz)]

    if(i<51):
        datx.append(X)
        i+=1
    else:
        i=0
        datx.clear()
    
    # print(datx)
    k=np.array(datx)
    if i==50:
        p1=k[:,0]
        p2=k[:,1]
        p3=k[:,2]
        p4=k[:,3]
        p5=k[:,4]
        p6=k[:,5]
        N = 50
        # sample spacing
        T = 1.0 / 100.0
        w = blackman(N)
        arr_x=[]
        arr_y=[]
        arr_z=[]
        arr_x1=[]
        arr_y1=[]
        arr_z1=[]
        lmt = round(len(p1)/N)                          #change here
        
        
        
        xfx = fft(p1*w)
        xfy = fft(p2*w)
        xfz = fft(p3*w)
        yfx = fft(p4*w)
        yfy = fft(p5*w)
        yfz = fft(p6*w)
        # t_var= abs((np.sqrt(np.array(yfx)**2 + np.array(yfy)**2 + np.array(yfz)**2)).reshape(-1,1))
        t_var= abs((np.sqrt(np.array(xfx)**2 + np.array(xfy)**2 + np.array(xfz)**2 )).reshape(-1,1))

        op_pred = loaded_model.predict(t_var.transpose())
        dev="DIAL"
        loc="ML_stat"
        # print(result)
        if op_pred == [1]:
            print("Working")
            mesg='1'
            var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=iot' --data-binary '"+dev+" "+loc+"="+mesg+"'"
            os.system(var)
            # count+=1
        elif op_pred == [2]:
            print("Inverted")
            mesg='2'
            var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=iot' --data-binary '"+dev+" "+loc+"="+mesg+"'"
            os.system(var)
            # count+=1
        else:
            print("Stopped")
            mesg='0'
            var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=iot' --data-binary '"+dev+" "+loc+"="+mesg+"'"
            os.system(var)
# ser_v.close()
sock.close()






