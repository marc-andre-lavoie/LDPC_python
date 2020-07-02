#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:36:23 2020

@author: Marc-Andre Lavoie
"""

import gallager_A_V2 as gal
import os

#import cProfile #xx#
#pr=cProfile.Profile() #xx#
# =============================================================================
# Initializing the parameters for the simulation
outputName="million"
matrices=[matrix for matrix in os.listdir("matrices_alireza") if ".txt"in matrix]
probabilities=(5,10,15,20,25,30)
trials=1000000
failed_stop=100
# =============================================================================

of=open("results/{}.txt".format(outputName),"a+")#Open in append mode and creates new file if needed
of.write("#=============================================#\n")
#pr.enable() #xx#
for matrixH in matrices:
    print("working on {}".format(matrixH))
    obj=gal.paritycheck("matrices_alireza/"+matrixH) #Create the object
    of.write("Results for {} :\n".format(matrixH))
    #of.write("\u03B1   \tBER\tSuccess\t\t\tFER\n")
    of.write("a   \tBER\tSuccess\t\t\tFER\n")
    for prob in probabilities:
        #while obj.failed<failed_stop:
        while obj.trial<trials:
            if obj.decoderZero(prob):
                obj.success+=1
            else : 
                obj.failed+=1
            if obj.trial%1000==0:
                print(obj.trial)
            obj.trial+=1
        of.write("{:.3f}\t{:.3f} \t{}/{}\t\t {} \n"
                 .format(prob/1000,obj.BER(),obj.success,obj.trial,obj.FER()))
        #get ready for other loop
        obj.resetCounters()
of.close()
#pr.disable() #xx#
#pr.print_stats() #xx#
print("Done")
