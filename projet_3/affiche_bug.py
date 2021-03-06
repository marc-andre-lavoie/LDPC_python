# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 11:35:10 2021

@author: marck
"""
from PIL import Image
import numpy as np


img=Image.open("stinkbug.png")
data=np.asarray(img)

pilImage = Image.fromarray(data,'RGB')
pilImage.save('my.png') #Sauvegarder l'image
pilImage.show() #Afficher l'image sur l'écran
data.tofile("jambon.bin") #FICHIER BINAIRE QUE J'UTILISERAI

#---------Lecture--------------#
file=open("jambon.bin","rb")
byte=file.read(1)
file.close()

lecture=np.fromfile("jambon.bin","uint8") #array a partir du fichier

# =============================================================================
#--------------Test 3D array#----------------#
# array_test=np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
# array_test.tofile("test_array.bin")
# lecture2=np.fromfile("test_array.bin","int32")
# =============================================================================
