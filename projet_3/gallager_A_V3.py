#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:59:15 2020

@author: marck
"""
#Create matrix H from Alireza's text file

import numpy as np
from pyldpc import make_ldpc
class paritycheck:
    
    def __init__(self):
        n=56
        dv=3
        dc=4
        self.H,G=make_ldpc(n,dv,dc)
        self.Ht=np.transpose(self.H)
        Gt=np.transpose(G)
        Gt=np.delete(Gt,-1,axis=0)
        Gt=np.delete(Gt,-1,axis=0)
        self.G=Gt
        
        #H and G created
# =============================================================================
#         Attributes
        self.m=self.H.shape[0]
        self.n=self.H.shape[1]
        self.k=self.n-self.m
        self.IT_MAX=18
        self.success=0
        self.failed=0
        self.flipped=0
        self.nbIter=[] #Not used yet
        self.trial=0
# =============================================================================
        
        self.dv=[]
        for i in range(0,self.n):                
            self.dv.append(self.H[:,i].tolist().count(1))
        
        
        
    def decoderZero (self,prob):
        u=np.ones(self.k)
        codeWord=(u@self.G)%2    
        noiseProb=np.random.randint(0,10000,self.n) # Random numbers between 0 and 100  
        
        ksiV=np.ones(self.n)-(2*codeWord)
        
        for i in range(0,self.n):
            if noiseProb[i]<prob:
                ksiV[i]*=-1
        #print("There are {} mistakes in the codeword".format(ksiV.tolist().count(-1))) #Only works for all-zero codeword 
        self.flipped+=ksiV.tolist().count(-1)#Only works for all-zero codeword
        #A lot of initializations
        nb_it=0
        vi=[]
        ksiC=np.ones((self.m,self.n),dtype="int")
        xDecoded=np.ones(self.n)
        #Emplacement des 1 sur les lignes
        for j in range(0,self.m):
            vi.append(np.nonzero(self.H[j,:])[0])
        
        ##Decoding
        
        previousx=np.zeros(self.n)
        #while nb_it==0 or (IT_MAX<nb_it and np.count_nonzero((H@xDecoded)%2)):
        while nb_it<self.IT_MAX and not np.array_equal(previousx,xDecoded):#not np.array_equal(xDecoded,codeWord):
        #Step 2
            previousx=xDecoded
        
            for j in range(0,self.m):        
                for i in vi[j]:
                    grosPi=1
                    for z in vi[j]:
                        if z != i:
                            grosPi=grosPi*ksiV[z]
                    ksiC[j][i]=grosPi #Message from CN to VN
        
                            
        #Step 3 (Majority voting)
            for i in range(0,self.n):
                nbNeg=ksiC[:,i].tolist().count(-1)
                if nbNeg == self.dv[i] and ksiV[i]==1: #xChapeau/ksiV
                    ksiV[i]=-1
                    
                elif nbNeg == 0 and ksiV[i]==-1: #xChapeau/ksiV
                    ksiV[i]=1
                    
            xDecoded = np.array([(x-1)/-2 for x in ksiV],dtype='int')
            nb_it+=1
        
        #print("Number of iterations : {}".format(nb_it))
        self.nbIter.append(nb_it)
        result=np.array_equal(xDecoded,codeWord)        
        #print("The decoding is successful : {}".format(result))
        
        return result

    def resetCounters(self):
        self.success=0
        self.failed=0
        self.flipped=0
        self.nbIter=[]
        self.trial=0
        
    def BER(self):
        return self.flipped/(self.n*self.trial)
    def FER(self):
        return self.failed/self.trial