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
    arr_r=[]
    for un_byte in byte_int:
        arr=[(un_byte>>i & 1) for i in range(7,-1,-1)]
        arr_r.append(arr)
    arr_r=np.array(arr_r).reshape(-1)
    if(len(arr_r)>108):
        arr_r=arr_r[:-4]
    return arr_r

def word_to_bytes(buf_send):
    c=7
    bit_sum=0
    arr_return=[]
    for i in buf_send:
        bit_sum+=i*(2**c)
        c-=1
        if c<0:
            c=7
            arr_return.append(bit_sum)
            bit_sum=0
    if(bit_sum!=0 or len(arr_return)==13): #A REGARDER
        arr_return.append(bit_sum)
    arr_return=bytes(arr_return)
    return arr_return 
def decode_GALA (H,x):
    n=108
    m=52
    k=56
    IT_MAX = 18
    dv=3
    dc=6
    ###Decoding part starts###
    ###Algorithm taken mostly from Fangping Ye, chapter 3, page 22-23###
    
    #Step 1 :Initialization
    ksiV=np.ones(n)
    ksiV=ksiV-(2*x) #Makes binary operations easier
    xChapeau=ksiV
    
    l=1
    #H=m1.H
    ci=np.nonzero(H)[0]
    vi=np.nonzero(H)[1] #Donne index de colonnes avec au moins un 1
    ksiC=np.ones((m,n),dtype="int")
    xDecoded=np.ones(n)
    xDecoded_p=np.zeros(n)
    #while np.array_equal(xDecoded,x) == False and l<IT_MAX: #While qui fct mais sketch
    while (not np.array_equal(xDecoded,xDecoded_p)) and l<IT_MAX:
        l+=1
    #Step 2
        for j in range(0,m):        
            for i in vi[dc*j : dc+dc*j]:
                grosPi=1
                for k in vi[dc*j : dc+dc*j]:
                    if k != i:
                        grosPi=grosPi*ksiV[k]
                ksiC[j][i]=grosPi #Message from CN to VN                      
    #Step 3 (Majority voting)
        for i in range(0,n):    
            nbNeg=ksiC[:,i].tolist().count(-1)
            if nbNeg>int(dv/2) and xChapeau[i]==1: #Supposed to be majority, doesn't work
            #if nbNeg == dv and xChapeau[i]==1:
                ksiV[i]=-1
                
            #elif nbNeg<=int(dv/2) and xChapeau[i]==-1:
            elif nbNeg == 0 and xChapeau[i]==-1:
                ksiV[i]=1
        xDecoded_p=xDecoded       
        xDecoded = np.array([(x-1)/-2 for x in ksiV],dtype='int')   
    return xDecoded
########################DEBUT CODE###############################
#On a 3 types de buffers : Bytes, bin, et empty qui contient les 3 pixels
##SETUP COMM##
ser=serial.Serial('/dev/ttyACM0',115200)#,timeout=1)
ser.flush()
##
#On prend l'info de l'image
img=Image.open("poly.jpg")
data=np.asarray(img)
data_line=data.reshape(-1)#On peut reshape pour reconstruire l'image aussi
data_line_rec=[]
data_good=[] # Tout le data binaire
data_bad=[]
H,G=get_H_G(0)

counter=0 #watchout counter 
while(counter<len(data_line)):
    buf_send=np.zeros(7,np.uint8)
    buf_send[0]=200#synchro
    for c in range(counter,counter+6):
        buf_send[c-counter+1]=data_line[c]
    counter+=6
    buf_send_bin=((get_bin_arr(buf_send))@G)%2#Binaire pour encodage
    data_good.append(buf_send_bin)
    buf_send_bytes=word_to_bytes(buf_send_bin)#Bytes pour envoie
    #data_coded.append([x for x in buf_send_bytes])
    buf_rec_bytes=[0] #On initialise
    ##Petit protocole pour bien envoyer par UART
    while(buf_rec_bytes[0]!=buf_send_bytes[0]): #On attend que la comm soit bient faite
        ser.write(buf_send_bytes)
        buf_rec_bytes=ser.read(14)#bits renvoyes par uc
    buf_rec_bytes=[x for x in buf_rec_bytes]#Bytes en tableau de int
    ##Fin du protocole de comm.
    #data_undecoded.append(buf_rec_bytes)
    buf_rec_bin=get_bin_arr(buf_rec_bytes)
    data_bad.append(buf_rec_bin)
    #On decode pour retrouver le mot initial
    buf_rec=np.concatenate((buf_rec_bin[0:35:1],buf_rec_bin[36:56:1]))
    buf_rec=np.append(buf_rec,buf_rec_bin[72])
    buf_rec=word_to_bytes(buf_rec)
    buf_rec=[x for x in buf_rec]#Bytes en tableau de int
    buf_rec.pop(0)#On enleve la synch
    #Fin du decodage pour mot initial
    data_line_rec.append(buf_rec)
    ######Debut code ajoute pour corr erreurs
    #data_undecoded.append(buf_rec_bin) #List of np arrays
    ######Fin code ajoute pour corr erreurs
    if(counter%1200==0):
        print(counter)
data_line_rec=np.array(data_line_rec).reshape(-1)
shape=data.shape
matrice_recue=np.reshape(data_line_rec,(shape[0],shape[1],shape[2]))
#matrice_recue=np.reshape(data_line_rec,(375,500,3))
matrice_recue=matrice_recue.astype('uint8')
pilImage = Image.fromarray(matrice_recue,'RGB')
pilImage.save('samedi_b_q8.png') #Sauvegarder l'image
##Image corr
print("-------Start correction--------")
data_line_c=[]
data_bad_c=[]
for i in range(len(data_bad)):
    if(not np.array_equal(data_bad[i],data_good[i])):
        buf=decode_GALA(H,data_bad[i])
    else:
        buf=data_bad[i]
    if(i%1000==0):
        print(i)
    #Code qui vient d'etre ajoute
    data_bad_c.append(buf) #Pour compter le BER apres correction
    buf_rec=np.concatenate((buf[0:35:1],buf[36:56:1]))
    buf_rec=np.append(buf_rec,buf[72])
    buf_rec=word_to_bytes(buf_rec)
    buf_rec=[x for x in buf_rec]#Bytes en tableau de int
    buf_rec.pop(0)#On enleve la synch
    #Fin du decodage pour mot initial
    data_line_c.append(buf_rec)

data_line_c=np.array(data_line_c).reshape(-1)
matrice_recue_c=np.reshape(data_line_c,(shape[0],shape[1],shape[2]))
#matrice_recue=np.reshape(data_line_rec,(375,500,3))
matrice_recue_c=matrice_recue_c.astype('uint8')
pilImagec = Image.fromarray(matrice_recue_c,'RGB')
pilImagec.save('samedi_c_q8.png') #Sauvegarder l'image    

#----------Data analysis--------------------------------#
flipped_bits_b=0
for i in range(len(data_good)):
    flipped_bits_b+=np.sum(data_good[i]!=data_bad[i])#On additionne pour tous les mots
    
BER_b=flipped_bits_b/(len(data_bad)*100)#BER avant correction, *100 car 108 bits-8 bits de synchro

flipped_bits_c=0
for i in range(len(data_good)):
    flipped_bits_c+=np.sum(data_good[i]!=data_bad_c[i])#On additionne pour tous les mots
BER_c=flipped_bits_c/(len(data_bad_c)*100)#BER apres correction

#FER
err_cnt=0
for i in range(0,len(data_line),3):
    if(data_line[i]!=data_line_c[i] or data_line[i+1]!=data_line_c[i+1] or data_line[i+2]!=data_line_c[i+2]):
        err_cnt+=1
FER=err_cnt/(len(data_line)/3)
print('FER : ',FER)

