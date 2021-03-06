# -*- coding: utf-8 -*-
# Project 1 for Numerical Algorithms
#Charles Rohart, Ingrid Odlen, Laroy Sjödahl, Niklas Lindeke
from numpy import *
from scipy import *
from matplotlib.pyplot import *

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
    def __init__(self, knot_sequence, controlpoints_sequence,nbpoints=1000):
        self.knot_sequence = array(knot_sequence)
        self.controlpoints_sequence = controlpoints_sequence
        self.nbpoints=nbpoints
        self.step=long((self.knot_sequence[self.knot_sequence.argmax()]-\
        self.knot_sequence[self.knot_sequence.argmin()]))/long(self.nbpoints)
        
    def __call__(self):
        listpointsx=array([])
        listpointsy=array([])
        u=self.knot_sequence[self.knot_sequence.argmin()]
        while (u<=self.knot_sequence[self.knot_sequence.argmax()] and\
        u>=self.knot_sequence[self.knot_sequence.argmin()]):
            try:
                listpointsx=append(listpointsx,self.blossom(u,0))
                listpointsy=append(listpointsy,self.blossom(u,1))
            except:
                None
            u+=self.step
        plot(listpointsx,listpointsy)
        plot(array(self.controlpoints_sequence)[:,0],array(self.controlpoints_sequence)[:,1],'ro--')      
        return 
        
    def blossom_old(self,u_in,xory):
        #this function is a try at making blossoms cleaner
        #u_in should be between u[2] and u[size(a)-3], in terms of size, leaving two elements at each edge so the iteration will stay within bounds
        I = self.findhot(u_in) - 1 #ui & not ui+1!!!
        u = self.knot_sequence
        d = self.controlpoints_sequence
        def alfa(u,u_l,u_r):
            return (u_r - u) / (u_r - u_l)   

        di=array([])
        di = append(di,[alfa(u_in,u[I-2+i],u[I+i+1])*d[I-2+i][xory]+\
        (1 - alfa(u_in,u[I-2+i],u[I+i+1])) * d[I-1+i][xory] for i in range(3)])
        di = append(di,[alfa(u_in,u[I-i+1],u[I+i+1]) * di[i] +\
        (1 - alfa(u_in,u[I-i+1],u[I+i+1])) * di[i+1] for i in range(2)])
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
        
    def blossom(self,u_in,xory):
        I = self.findhot(u_in) - 1 #ui & not ui+1!!!
        u = self.knot_sequence
        d = self.controlpoints_sequence
        def alfa(u,u_l,u_r):
            return (u_r - u) / (u_r - u_l)   
        d_1 = alfa(u_in,u[I-2],u[I+1]) * d[I-2][xory] + (1 - alfa(u_in,u[I-2],u[I+1])) * d[I-1][xory]
        d_2 = alfa(u_in,u[I-1],u[I+2]) * d[I-1][xory] + (1 - alfa(u_in,u[I-1],u[I+2])) * d[I][xory]
        d_3 = alfa(u_in,u[I],u[I+3]) * d[I][xory] +     (1 - alfa(u_in,u[I],u[I+3])) * d[I+1][xory]

        d_1_2 = alfa(u_in,u[I-1],u[I+1]) * d_1 + (1 - alfa(u_in,u[I-1],u[I+1])) * d_2
        d_2_2 = alfa(u_in,u[I],u[I+2]) * d_2 + (1 - alfa(u_in,u[I],u[I+2])) * d_3  
        
        ds = alfa(u_in,u[I],u[I+1]) * d_1_2 + (1 - alfa(u_in,u[I],u[I+1])) * d_2_2  
        return ds
        
#  two test-cases for the BSpline project


def spline(clamped=True):

    control_points = [(-12.73564, 9.03455),
    (-26.77725, 15.89208),
    (-42.12487, 20.57261),
    (-15.34799, 4.57169),
    (-31.72987, 6.85753),
    (-49.14568, 6.85754),
    (-38.09753, -1e-05),
    (-67.92234, -11.10268),
    (-89.47453, -33.30804),
    (-21.44344, -22.31416),
    (-32.16513, -53.33632),
    (-32.16511, -93.06657),
    (-2e-05, -39.83887),
    (10.72167, -70.86103),
    (32.16511, -93.06658),
    (21.55219, -22.31397),
    (51.377, -33.47106),
    (89.47453, -33.47131),
    (15.89191, 0.00025),
    (30.9676, 1.95954),
    (45.22709, 5.87789),
    (14.36797, 3.91883),
    (27.59321, 9.68786),
    (39.67575, 17.30712)]
    grid = linspace(0, 1, 26)
    if clamped:
        grid[ 1] = grid[ 2] = grid[ 0]
        grid[-3] = grid[-2] = grid[-1]
    return (control_points, grid)