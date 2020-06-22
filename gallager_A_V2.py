# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:59:15 2020

@author: marck
"""
#Create matrix H from Alireza's text file

import numpy as np

matrixText = open("Code1_MinDis8_Girth6_Dimen56_Rate0518_Length108.txt", "r")
lines=matrixText.readlines()

bigList=[]
for line in lines:
    
    if 'G' in line:
        break
    if line[0]!='[':
        continue
    
    matList=[num for num in line if num.isnumeric()]
    bigList.append(matList)
    

H=np.array(bigList,dtype='int')

#H created
m=H.shape[0]
n=H.shape[1]
k=n-m
    
codeWord=np.zeros(n)    
noiseProb=np.random.randint(0,100,n) # Random numbers between 0 and 100  

ksiV=np.ones(n)-(2*codeWord)

for i in range(0,n):
    if noiseProb[i]<2:
        ksiV[i]*=-1
print("There are {} mistakes in the codeword".format(ksiV.tolist().count(-1))) #Only works for all-zero codeword 

#A lot of initializations
xChapeau=ksiV
nb_it=0
IT_MAX=18
vi=[]
ksiC=np.ones((m,n),dtype="int")
xDecoded=np.ones(n)
#
#Emplacement des 1 sur les lignes
for j in range(0,m):
    vi.append(np.nonzero(H[j,:])[0])

##Decoding

previousx=np.zeros(n)
#while nb_it==0 or (IT_MAX<nb_it and np.count_nonzero((H@xDecoded)%2)):
while nb_it<IT_MAX and not np.array_equal(previousx,xDecoded):#not np.array_equal(xDecoded,codeWord):
#Step 2
    previousx=xDecoded

    for j in range(0,m):        
        for i in vi[j]:
            grosPi=1
            for z in vi[j]:
                if z != i:
                    grosPi=grosPi*ksiV[z]
            ksiC[j][i]=grosPi #Message from CN to VN

                    
#Step 3 (Majority voting)
    for i in range(0,n):
        
        dv=H[:,i].tolist().count(1)

        nbNeg=ksiC[:,i].tolist().count(-1)
        if nbNeg == dv and ksiV[i]==1: #xChapeau/ksiV
            ksiV[i]=-1
            
        elif nbNeg == 0 and ksiV[i]==-1: #xChapeau/ksiV
            ksiV[i]=1
            
    xDecoded = np.array([(x-1)/-2 for x in ksiV],dtype='int')
    nb_it+=1

print("Number of iterations : {}".format(nb_it))        

print("The decoding is successful : {}".format(np.array_equal(xDecoded,codeWord)))
