from numpy import *
from scipy import *

def f(x):
    """
    Create any form of Objective function
    """
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    Objective = x1**2 - 2.0 * x1 * x2 + 4 * x2**2 + 3*x3
    return Objective
    
def ddx(fx):
    """
    Returns a Gradient Vector
    """
    Gradient = gradient(fx)
    return Gradient
    
def d2dx(x):
    """
    Returns the Hessian Vector
    """
    Hessian = gradient(ddx(f(x)))
    return Hessian
    

class OPC:
    """
    Some stuff
    """
    
    def __init__(self, obj_func, grad=None):
        self.obj_func = obj_func
        self.grad = grad
    
    class QN(OPC):
        def __call__(self):
            return False
    
    
    class LS(OPC):
        class E:
            def __call__(self):
                return False
            
        class IE:
            def __call(self):
                return False