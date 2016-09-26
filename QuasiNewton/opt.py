from numpy import *
from scipy import *

def f():
    x,y,z = mgrid[0:101:25., 0:101:25., 0:101:25.]
    obj = 2*x**2 + 3*y**2 - 4*z 
    return obj
    
def dfdx():
    grad = gradient(f())
    return grad
    
def df2dx():
    hess = gradient(dfdx())
    return hess

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
        termination_criterion=False
        while termination_criteron!=True:
            x=x-NewtonDirection(x)
            k=k+1
    def NewtonDirection(x):
        return InvHessian(x)*Gradient(x)
    def InvHessian(x):
    def Gradient(x):
        if grad!=None:
            return grad
        else:
            
            
    
class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        