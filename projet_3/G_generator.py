# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 10:54:58 2021

@author: marck
"""

import numpy as np
import os
import random

###Variables
n=108
m=52
k=56
IT_MAX = 18
dv=3
dc=6

##Reading the matrices
matrices=[matrix for matrix in os.listdir("matrices_alireza") if ".txt"in matrix]
matrixText = open("matrices_alireza/"+matrices[1],"r")
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

### Add noise here

noise = np.zeros(n)
noise[random.randint(0,n-1)]=1 # 1 bit flipped
noise[random.randint(0,n-1)]=1 # 2 bits flipped
#noise[random.randint(0,n-1)]=1 # 2 bits flipped
### Noisy message
y=(x+noise)%2

    
print("With noise :{}".format(y.astype('int')))

###Decoding part starts###
###Algorithm taken mostly from Fangping Ye, chapter 3, page 22-23###

#Step 1 :Initialization
ksiV=np.ones(n)
ksiV=ksiV-(2*y) #Makes binary operations easier
xChapeau=ksiV

l=1
#H=m1.H
ci=np.nonzero(H)[0]
vi=np.nonzero(H)[1] #Donne index de colonnes avec au moins un 1
ksiC=np.ones((m,n),dtype="int")
xDecoded=np.ones(n)
while np.array_equal(xDecoded,x) == False and l<IT_MAX:
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
        #if nbNeg>int(dv/2) and xChapeau[i]==1: #Supposed to be majority, doesn't work
        if nbNeg == dv and xChapeau[i]==1:
            ksiV[i]=-1
            
        #elif nbNeg<=int(dv/2) and xChapeau[i]==-1:
        elif nbNeg == 0 and xChapeau[i]==-1:
            ksiV[i]=1
            
    xDecoded = np.array([(x-1)/-2 for x in ksiV],dtype='int')        
    print("Next iteration")
    


print("The decoding is successful : {}".format(np.array_equal(xDecoded,x)))