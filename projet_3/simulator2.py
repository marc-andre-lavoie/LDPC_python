# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 13:58:55 2021

@author: marck
"""
import gallager_A_V3 as gal

outputName="projet_3"
probabilities=(10,100,10000)# a=prob/10000
trials=5000
failed_stop=100
# =============================================================================

of=open("results/{}.txt".format(outputName),"a+")#Open in append mode and creates new file if needed
of.write("#=============================================#\n")
#pr.enable() #xx#
obj=gal.paritycheck() #Create the object
#of.write("Results")
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
             .format(prob/10000,obj.BER(),obj.success,obj.trial,obj.FER()))
    #get ready for other loop
    obj.resetCounters()
of.close()
#pr.disable() #xx#
#pr.print_stats() #xx#
print("Done")