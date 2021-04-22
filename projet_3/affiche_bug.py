# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 11:35:10 2021

@author: marck
"""
from PIL import Image
import numpy as np

#print("Quelle matrice?")
#path_matrice=filedialog.askopenfilename()
img=Image.open("Resultats_rapport/samedi_c_q4.png")
data=np.asarray(img)
data_line=data.reshape(-1)

img_init=Image.open("poly.jpg")
data_init=np.asarray(img_init)
data_line_init=data_init.reshape(-1)

err_cnt=0
for i in range(0,len(data_line_init),3):
    if(data_line[i]!=data_line_init[i] or data_line[i+1]!=data_line_init[i+1] or data_line[i+2]!=data_line_init[i+2]):
        err_cnt+=1
FER=err_cnt/(len(data_line)/3)
print('FER : ',FER)

#---------Lecture--------------#
#file=open("jambon.bin","rb")
#byte=file.read(1)
#file.close()

#lecture=np.fromfile("jambon.bin","uint8") #array a partir du fichier

# =============================================================================
#--------------Test 3D array#----------------#
# array_test=np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
# array_test.tofile("test_array.bin")
# lecture2=np.fromfile("test_array.bin","int32")
# =============================================================================
