from numpy import *
from scipy import *
import scipy.linalg as lin

class Room:
    def __init__(self,nbroom,uh=40,uw=15,uwf=5,dx=1/3,dimx=1,dimy=1,omega=0.8):
        self.uh=uh
        self.uw=uw
        self.uwf=uwf
        self.dx=dx
        self.dimx=dimx
        self.dimy=dimy
        self.nbroom=nbroom
        self.omega=omega
        self.dimxx=int(dimx/dx)
        self.dimyy=int(dimy/dx)
        self.matrice=self.matrice_func()
    def matrice_func(self):
        matrice=empty((self.dimyy+1,self.dimxx+1))
        if self.nbroom!=2:
            for i in range(self.dimyy+1):
                if self.nbroom==1:
                    matrice[0,i]=self.uw
                    matrice[self.dimxx,i]=self.uw
                    matrice[i,0]=self.uh
                if self.nbroom==3:
                    if not i==self.dimxx: matrice[0,i]=self.uw
                    matrice[self.dimxx,i]=self.uw
                    matrice[i,self.dimyy]=self.uh
        elif self.nbroom==2:
            for j in range(self.dimyy+1):
                matrice[j,0]=self.uw
                matrice[j,self.dimxx]=self.uw
            for i in range(self.dimxx+1):
                matrice[0,i]=self.uh
                matrice[self.dimyy,i]=self.uwf
        return matrice
    def compute_func(self):
        for i in range(self.dimyy+1):
            for j in range(self.dimxx+1):
                None