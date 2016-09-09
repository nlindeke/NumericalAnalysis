# Project 1 for Numerical Algorithms
import numpy as np
import scipy as sp

class CSplines:
    """
        Implementation of the De Boor Algorithm for Cubic Splines.
        
        Some general information about the code so that Claus will be pleased 
        with the amount of documentation.
        
        input:
            knot_sequence: u
            
        output:
            spline: s(u)
            
    """
    def __init__(self,nodepoints):
        self.nodepoints = nodepoints
    
    def __call__(self):
        return # something
    
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
        
    def basisfunc(self, knots):
        return # something
        
    def findhot(self):
        a = np.array([1,2,3,4])
        u = 3.
        i = (a > u).argmax()
        return i
        
    #Git commit test
    def countAllTheNumbers(self):
        a=0        
        while True:
           a=a+1 