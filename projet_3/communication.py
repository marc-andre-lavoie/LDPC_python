#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:05:30 2021

@author: pi
"""

import RPi.GPIO as GPIO
import numpy as np
import os
#import serial

#ser=serial.Serial("/dev/ttyAMA0")
#ser.baudrate=9600
#ser.write('sup'.format())
#data=ser.read(1)
#import time
#Preparation de GPIO
GPIO.setmode(GPIO.BOARD)
outPin=7
clkin=5
GPIO.setup(clkin,GPIO.IN)
GPIO.setup(outPin,GPIO.OUT)
#fin GPIO
###Variables
n=108
m=52
k=56
IT_MAX = 18
dv=3
dc=6

##Reading the matrices
matrices=[matrix for matrix in os.listdir("matrices_alireza") if ".txt"in matrix]
matrixText = open("matrices_alireza/"+matrices[0],"r")
lines=matrixText.readlines()
bigListH=[]
bigListG=[]
is_g=0
for line in lines:
    
    if 'G' in line:
        is_g=1
        continue
    elif line[0]!='[':
        continue
    elif is_g==0:
        matList=[num for num in line if num.isnumeric()]
        bigListH.append(matList)
    else:
        matList=[num for num in line if num.isnumeric()] 
        bigListG.append(matList)

H=np.array(bigListH,dtype='int')
G=np.array(bigListG,dtype='int')

##Encoding
u=np.random.randint(0,2,k) #The message
x=(u@G)%2 # encoding the message

print("No noise :  {}".format(x))
#SEND THE INFO
started=0
for i in x:
 
     GPIO.wait_for_edge(clkin,GPIO.RISING)
     if (started==0):
         #print("go")
         started=1
     GPIO.output(outPin,bool(i))


GPIO.cleanup();
print("Envoie termine")