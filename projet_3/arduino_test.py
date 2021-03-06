#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:01:32 2021

@author: pi
"""

import serial
#import time

ser=serial.Serial('/dev/ttyACM2',9600,timeout=1)
ser.flush()
#time.sleep(1)
while True:
    if ser.in_waiting > 0 :
        ser.write(b'abcdefg')
        recu=ser.read(7)
        print(recu)
        line=ser.readline().decode('utf-8').rstrip()#rstrip sert a enlever les EOL
        print(line)