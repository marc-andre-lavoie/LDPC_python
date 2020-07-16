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
outputName="temp"
matrices=[matrix for matrix in os.listdir("matrices_alireza") if ".txt"in matrix]
probabilities=(0.0001,0.001)
trials=10000
failed_stop=100
#Keep track of progress
done=0
progress=0
total=len(probabilities)*len(matrices)*trials
# =============================================================================

of=open("results/{}.txt".format(outputName),"a+")#Open in append mode and creates new file if needed
of.write("#=============================================#\n")
for matrixH in matrices:
    print("working on {}".format(matrixH))
    obj=gal.paritycheck("matrices_alireza/"+matrixH) #Create the object
    of.write("Results for {} :\n".format(matrixH))
    #of.write("\u03B1   \tBER\tSuccess\t\t\tFER\n")
    of.write("a   \tBER\tSuccess\t\t\tFER\tavg it\n")
    for prob in probabilities:
        #while obj.failed<failed_stop:
        while obj.trial<trials:
            if obj.decoderZero(prob):
                obj.success+=1
            else : 
                obj.failed+=1
            if obj.trial%1000==0:
                progress=(done*trials+obj.trial)/trials
                print("{}%".format(progress))
            obj.trial+=1
        of.write("{:.3f}\t{:.3f} \t{}/{}\t\t {}\t{} \n"
                 .format(prob,obj.BER(),obj.success,obj.trial,obj.FER(),obj.avg_it()))
        #get ready for other loop
        obj.resetCounters()
        done+=1
of.close()

print("Done")
