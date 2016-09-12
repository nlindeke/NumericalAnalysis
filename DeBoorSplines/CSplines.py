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
            
        output:
            spline: s(u)
            
    """
    def __init__(self,knot_sequence, controlpoints_sequence):
        self.knot_sequence = knot_sequence
        self.controlpoints_sequence = controlpoints_sequence
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
        
    def basisfunc(self, knot_sequence):
        return # something
        
    def findhot(self,u_in):
        return (self.knot_sequence > u_in).argmax()
        """
           Return the starting index for a given u in the knot sequence.
           Same as before, just less verbose.
        """
 