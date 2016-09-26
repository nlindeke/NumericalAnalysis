from numpy import *
from scipy import *

def f(x):
    """
    Create any form of Objective function with input matrix x
    
    We should later on construct this so we can make a function of
    a varying amount of variables
    """
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    Objective = x1**3 - 2.0 * x1**2 * x2 + 4 * x2**2 + 3*x3
    return Objective
    
def ddx(fx):
    """
    Returns a Gradient Vector
    """
    Gradient = gradient(fx)
    return Gradient
    

class OPC:
    """
    Some stuff
    """
    
    def __init__(self, obj_func, grad=None):
        self.obj_func = obj_func
        self.grad = grad
    
    def d2dx():
        """
        Returns the Hessia, which is the gradient of the gradient vector
        """
        if self.grad != None:
            return gradient(self.grad)
        else: return gradient(ddx(self.obj_func))
    
    class QN(OPC:
        def __call__(self):
            return False
    
    
    class LS(OPC):
        class E:
            def __call__(self):
                return False
            
        class IE:
            def __call(self):
                return False