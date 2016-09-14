# Project 1 for Numerical Algorithms
from numpy import *
from scipy import *

class CSplines:
    """
        Implementation of the De Boor Algorithm for Cubic Splines.
        
        Some general information about the code so that Claus will be pleased 
        with the amount of documentation.
        
        input:
            knot_sequence: u
            controlpoints_sequence: 
            
        output:
            spline: s(u)
            
    """
    def __init__(self, knot_sequence, controlpoints_sequence,nbpoints=7.0):
        self.knot_sequence = array(knot_sequence)
        self.controlpoints_sequence = controlpoints_sequence
        self.nbpoints=nbpoints
        self.step=long((self.knot_sequence[self.knot_sequence.argmax()]-self.knot_sequence[self.knot_sequence.argmin()]))/long(self.nbpoints)
        
    def __call__(self):
        print self.step

        for u in range(self.knot_sequence[0], self.knot_sequence[self.knot_sequence.argmax()],self.step):
            I=self.findhot(u)-1 #ui & not ui+1!!!
            diminus2=[u(I-2),u(I-1),u(I)]
        return "hej"
        
    def blossom(self,u_in):
       
        I = self.findhot(u_in) - 1
        u = self.knot_sequence
        d = self.controlpoints_sequence

        def alfa(u,u_l,u_r):
            return (u_r - u) / (u_r - u_l) 

        d_1 = alfa(u_in,u[I-2],u[I+1]) * d[I-2] + (1 - alfa(u_in,u[I-2],u[I+1])) * d[I-1]
        d_2 = alfa(u_in,u[I-1],u[I+2]) * d[I-1] + (1 - alfa(u_in,u[I-1],u[I+2])) * d[I]
        d_3 = alfa(u_in,u[I],u[I+3]) * d[I] +     (1 - alfa(u_in,u[I],u[I+3])) * d[I+1]

        d_1_2 = alfa(u_in,u[I-1],u[I+1]) * d_1 + (1 - alfa(u_in,u[I-1],u[I+1])) * d_2
        d_2_2 = alfa(u_in,u[I],u[I+2]) * d_2 + (1 - alfa(u_in,u[I],u[I+2])) * d_3  
        
        ds = alfa(u_in,u[I],u[I+1]) * d_1_2 + (1 - alfa(u_in,u[I],u[I+1])) * d_2_2    
        
        #Här nedanför är ett snabbt alternativ, absolut inte genomtänkt, men marginellt kortare och nu med loop(tm)
        #man kan säkert baka ihop det ännu mer om man orkar.
        di=array()
        for i in range(3):
            di = di.append(alfa(u_in,u[I-2+i],u[I+i+1])*d[I-downIndex]+ (1 - alfa(u_in,u[I-2+i],u[I+i+1])) * d[I-1+i])
        for i in range(2):
           di.append(alfa(u_in,u[I-i+1],u[I+i+1]) * di[i] + (1 - alfa(u_in,u[I-i+1],u[I+i+1])) * di[i+1])
        return alfa(u_in,u[I],u[I+1]) * di[3] + (1 - alfa(u_in,u[I],u[I+1])) * di[4]
    

    
    def plotmethod(self, basis = True):
        """
            When basis is True (default) plotmethod plots 
            the basis function, when false, plotmethod 
            plots the control polygon
        """
        if(basis==True):
            # Plot thing
            return #
            
        elif(basis==False):
            # Plot other thing
            return #
            
        else:
            return False
        
    def basicfunc_tmp(self, eps, indice):
        #needs an exception for indice=0
        if indice==0:
            if eps==0 or eps==1:
                return 1
            else:
                return 0
        elif self.knot_sequence[indice-1]==self.knot_sequence[indice]:
            return 0
        elif self.knot_sequence[eps]>=self.knot_sequence[indice-1] and \
        self.knot_sequence[eps]<self.knot_sequence[indice]:
            return 1
        else:
            return 0
    def basicfunc(self, eps, indice, exponent=3):
        u=self.knot_sequence
        try:
            if exponent==0:
                return self.basicfunc_tmp(0,indice)
            else:
                return ((u[eps]-u[exponent-1])/(u[indice+exponent-1]-u[indice-1]))\
                *self.basicfunc(eps, indice, exponent-1)\
                + ((u[exponent+indice]-u[eps])/(u[exponent+indice]-u[indice]))\
                *self.basicfunc(eps, indice+1,exponent-1)
        except ZeroDivisionError:
            return 0
    def basicfunc_glob(self):
        listN=[]
        matrice=array([])
        for eps in range (0,self.knot_sequence.argmax() + 1):
            for indice in range(0,self.knot_sequence.argmax()+1):
                listN+=self.basicfunc(eps, indice)
            matrice+=listN
        return matrice
        
    def s(self,u,matrice):
        return matrice[u]
            
    def findhot(self,u_in):
        """
           Return the starting index for a given u in the knot sequence.
           Same as before, just less verbose.
        """        
        return (self.knot_sequence > u_in).argmax()
 