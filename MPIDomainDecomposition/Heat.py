from numpy import *
from scipy import *
import scipy.linalg as lin

class Room:
    def __init__(self,nbroom,uh=40,uw=15,uwf=5,dx=1.0/3,dimx=1,dimy=1,omega=0.8,tmptemp=16):
        self.uh=uh
        self.uw=uw
        self.uwf=uwf
        self.dx=dx
        self.dimx=dimx
        self.dimy=dimy
        self.nbroom=nbroom
        self.omega=omega
        self.tmptemp=tmptemp
        self.dimxx=int(dimx/dx)
        self.dimyy=int(dimy/dx)
        self.matrice=self.matrice_func()
    def matrice_func(self):
        matrice=zeros((self.dimyy+1,self.dimxx+1))
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
        matric=zeros(((self.dimxx+1)*(self.dimyy+1),(self.dimxx+1)*(self.dimyy+1)))
        if self.nbroom==2:
            dim=(self.dimxx-1)*(self.dimyy-1)
        else:
            dim=(self.dimxx-1)*(self.dimyy)
        #print (dim)
        k=0
        """
        for j in range(1,self.dimyy):
            for i in range(1,self.dimxx):
                None
        """
        for k in range(0,(self.dimxx+1)*(self.dimyy+1)):
            #uij+1 + uij-1 - 4uij + ui+1j + ui-1j
            i=k//(self.dimxx+1)
            j=k%(self.dimxx+1)
            for k2 in range(0,(self.dimxx+1)*(self.dimyy+1)):
                i2=k2//(self.dimxx+1)
                j2=k2%(self.dimxx+1)
                """
                print ("_____________")
                print ("i")
                print (i)
                print (i2)
                print ("j")
                print (j)
                print (j2)
                print ("_____________")
                """
                if i2==i and j2==j+1:
                    matric[k][k2]=1
                elif i2==i and j2==j-1:
                    matric[k][k2]=1
                elif i2==i and j2==j:
                    matric[k][k2]=-4
                elif i2==i+1 and j2==j:
                    matric[k][k2]=1
                elif i2==i-1 and j2==j:
                    matric[k][k2]=1
        l=0
        matric2=matric
        print(matric)
        arrayb=zeros((dim,1))
        for k in range(0,(self.dimxx+1)*(self.dimyy+1)):
            i=k//(self.dimxx+1)
            j=k%(self.dimxx+1)
            if self.matrice[i,j]!=0:
                matric2=delete(matric2,(l),0)
                l-=1
            l+=1
        l=0
        for k in range(0,(self.dimxx+1)*(self.dimyy+1)):
            i=k//(self.dimxx+1)
            j=k%(self.dimxx+1)
            if self.matrice[i,j]!=0:
                for m in range(dim):
                    if matric2[m,l]!=0:
                        arrayb[m,0]+=-1*self.matrice[i,j]
                matric2=delete(matric2,(l),1)
                l-=1
            l+=1
        m=0
        for i in range(self.dimyy+1):
            for j in range(self.dimxx+1):
                if (i!=0 and i!=self.dimyy) and ((j!=0 and self.nbroom==1) or (j!=self.dimxx and self.nbroom==3) or (j!=0 and j!=self.dimxx and self.nbroom==2)):
                    print(i,j)                    
                    arrayb[m,0]-=self.tmptemp
                    m+=1
        """
        print(matric)
        print(matric2)
        print(arrayb)
        """
        arraysol=lin.solve(matric2,arrayb)
        #print(arraysol)
        m=0
        for i in range(self.dimyy+1):
            for j in range(self.dimxx+1):
                if (i!=0 and i!=self.dimyy) and ((j!=0 and self.nbroom==1) or (j!=self.dimxx and self.nbroom==3) or (j!=0 and j!=self.dimxx and self.nbroom==2)):                   
                    self.matrice[i,j]=arraysol[m]
                    m+=1
        #print(self.matrice)
            