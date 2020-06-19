#Marc-Andre Lavoie, Project Ef-fective
import numpy as np
import random
from sympy import Matrix

###Variables chosen initially###
IT_MAX = 100
dv=3 #Raisonnable, pour les colonnes
dc=4 #Raisonnable, pour les lignes
n=20#Arbitraire
m=int((n*dv)/dc)
k=n-m
###


class randomH:
    H=None
    
    def __init__(self):
        self.H=np.zeros((m,n),dtype="int")
        
        for i in range(0,m-dv):
            while (np.count_nonzero(self.H[i,:]) < dc ):
                nb=random.randint(0,n-1)
                if(np.count_nonzero(self.H[:,nb]) < dv):
                    self.H[i][nb]=1
                    
        #Modifié à partir d'ici, pour eviter les loops interminables
        x = range(1,dv+1)
        for i in range(m-dv, m):
            for j in range(0, n): #verify each column
                    if np.count_nonzero(self.H[:,j])<x[i-(m-dv)]:
                        self.H[i][j]=1
            while np.count_nonzero(self.H[i,:]) < dc :
                nb=random.randint(0,n-1)
                if(np.count_nonzero(self.H[:,nb]) < dv):
                    self.H[i][nb]=1
                    
    def printMatrix(self):
        print(self.H)
        
    def nonZeroCount(self):
        return np.count_nonzero(self.H)
    
    def getHTransposed(self):
        return np.transpose(self.H)




det=0

### Generate random H matrix ###
while abs(det)<1 or int(round(det,0)%2) == 0 : #On veut une matrice avec la matrice sous-matrice B inversible
    m1=randomH()
    
    
    A=m1.H[:,0:k]
    B=m1.H[:,k:n]
    Bt=np.transpose(B)
    
    At=np.transpose(A)
    det=np.linalg.det(Bt)
    print('Det : {}'.format(det))
###

### Create Generator matrix ###
Bt=Matrix(Bt) # Matrix object from sympy
Btinv=Bt.inv_mod(2) #Modulo 2 invert takes a lot of time, should fix someday
Btinv=np.array(Matrix.tolist(Btinv)).astype(np.int) #On remet la matrice en np.array

Ik=np.eye(k)
Ik=Ik.astype('int')
temp=(At@Btinv)%2
temp=temp.astype('int')
G=np.concatenate((Ik,temp),axis=1)
#print(G)
grosTest=G@m1.getHTransposed() #Verify G*H^=0

if np.count_nonzero(grosTest%2) == 0:
    print("H and G matrices are successfully generated")

###

u=np.random.randint(0,2,k) #The message

x=(u@G)%2 # encoding the message

print("No noise :  {}".format(x))

### Add noise here

noise = np.zeros(n)
noise[random.randint(0,n-1)]=1
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
H=m1.H
ci=np.nonzero(H)[0]
vi=np.nonzero(H)[1]
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
        

