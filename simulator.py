#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:36:23 2020

@author: Marc-Andre Lavoie
"""

import gallager_A_V2 as gal
import os

# =============================================================================
# Initializing the parameters for the simulation
outputName="x6"
matrices=[matrix for matrix in os.listdir("matrices_alireza") if ".txt"in matrix]
probabilities=(1,2,3,4,5)
trials=128
failed_stop=100
# =============================================================================


of=open("results/{}.txt".format(outputName),"a+")#Open in append mode and creates new file if needed
of.write("#=============================================#\n")
for matrixH in matrices:
    print("working on {}".format(matrixH))
    obj=gal.paritycheck("matrices_alireza/"+matrixH) #Create the object
    of.write("Results for {} :\n".format(matrixH))
    of.write("\u03B1   \tBER\tSuccess\t\t\tFER\n")
    for prob in probabilities:
        while obj.failed<failed_stop:
            if obj.decoderZero(prob):
                obj.success+=1
            else : 
                obj.failed+=1
            obj.trial+=1
        of.write("{}\t{:.3f} \t{}/{}\t\t {} \n"
                 .format(prob,obj.BER(),obj.success,obj.trial,obj.FER()))
        #get ready for other loop
        obj.resetCounters()
of.close()
print("Done")
