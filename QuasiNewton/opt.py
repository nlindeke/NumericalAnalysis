from numpy import *
from scipy import *

class OPC:
    """
    Some stuff
    """
    def __init__(self, obj_func, grad=None):
        self.obj_func = obj_func
        self.grad = grad
    def base_newton(self,xzero):
        x=xzero
        k=0
        while termination_criteron!=True:
            x=x-NewtonDirection(x)
            k=k+1
    def NewtonDirection(x):
        return InvHessian(x)*Gradient(x)
    def InvHessian(x):
    def Gradient(x):
            
    
class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        
    