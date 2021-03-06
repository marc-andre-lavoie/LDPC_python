#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Mar  4 19:49:30 2021

@author: pi
"""
from PIL import Image
import numpy as np
import os
import serial

def get_H_G (select):   
    ##Reading the matrices
    matrices=[matrix for matrix in os.listdir("matrices_alireza") if ".txt"in matrix]
    matrixText = open("matrices_alireza/"+matrices[select],"r")
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
    return H,G
def get_bin_arr(byte_int):
    arr=[(byte_int>>i & 1) for i in range(7,-1,-1)]
    return arr

def word_to_bytes(buf_send):
    c=7
#    s=''
    bit_sum=0
    arr_return=[]
    for i in buf_send:
        bit_sum+=i*(2**c)
        c-=1
        if c<0:
            c=7
#            s=s+chr(bit_sum)
            arr_return.append(bit_sum)
            bit_sum=0
#    s=s+chr(bit_sum)#dernier octet
#    return bytes(s,'utf-8')
    if(bit_sum!=0): #A REGARDER
        arr_return.append(bit_sum)
    arr_return=bytes(arr_return)
    return arr_return 

########################DEBUT CODE###############################
##SETUP COMM##
ser=serial.Serial('/dev/ttyACM1',9600,timeout=1)
ser.flush()
##
#On prend l'info de l'image
img=Image.open("stinkbug.png")
data=np.asarray(img)
data_line=data.reshape(-1)#On peut reshape pour reconstruire l'image aussi
H,G=get_H_G(0)

counter=0
buf_send=[]
data_line_receive=[]#APRES DECODAGE
while (counter<np.size(data_line)): #On oarcourt tout l'image
    ##on prend 7 octets
    buf_send.append(get_bin_arr(data_line[counter]))
    counter+=1
    if(counter % 7 == 0): #ON PREND LES 7 PREMIERS BYTES
        buf_send=np.array(buf_send).reshape(-1)
        mot_code_send=(buf_send@G)%2 # on a maintenant le mot de code
        buf_send=word_to_bytes(mot_code_send)
        ser.write(buf_send)
        buf_rec=ser.read(14)#bits renvoyes par uc
        buf_rec=[x for x in buf_rec]#Bytes en tableau de int
        mot_code_rec=[]
        for x in buf_rec:
            mot_code_rec.append(get_bin_arr(x)) 
        mot_code_rec=np.array(mot_code_rec).reshape(-1)
        mot_code_rec=mot_code_rec[:-4]#DECODE
        ##Decode
        ##Decode
        ##Fill data_line_receive
        inter=np.concatenate((mot_code_rec[0:35:1],mot_code_rec[36:56:1]))
        inter=np.append(inter,mot_code_rec[72])
        bytes_inter=word_to_bytes(inter)
        buf_send=[] #ON RECOMMENCE POUR 56 AUTRES BITS
    
    
