# Project 1 for Numerical Algorithms
import numpy as np
import scipy as sp

class CSplines:
    """
        Implementation of the De Boor Algorithm for Cubic Splines.
        
        
        Some general information about the code so that Claus will be pleased 
        with the amount of documentation.
        
        input:
            nodepoints or u_vector / knot_vector
            
        output:
            s(u) (or something)
            
    """
    
    def __init__(self,nodepoints):
        self.nodepoints = nodepoints
    
    def __call__(self):
        return # something
        
    def basisfunc(self, knots):
        return # something
        
    def findhot(self, a):
        a = np.array([1,2,3,4])
        u = 3.
        i = (a > u).argmax()
        return i
        
    #Git commit test
    def countAllTheNumbers(self):
        a=0        
        while True:
           a=a+1 