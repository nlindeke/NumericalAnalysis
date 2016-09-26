from numpy import *
from scipy import *

def f():
    x,y = mgrid[0:101:50, 0:101:50]
    obj = 2*x**3 + 3*y**2
    return obj
    
def dfdx():
    grad = gradient(f())
    return grad
    
def df2dx():
    hess = gradient(dfdx())
    return hess
    

h = hessian()

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
        while termination_criterion!=True:
            x=x-self.NewtonDirection(x)
            k=k+1
            if x<=0.0001 and x>=-0.0001:
                termination_criterion=True
        return x
    def NewtonDirection(self,x):
        return self.InvHessian(x)*self.Gradient(x)
        
    def InvHessian(self,x):
        return numpy.linagl.inv(hessian())
        
    def hessian(self):
        x = f()
        x_grad = gradient(x) 
        hessian = empty((x.ndim, x.ndim) + x.shape, dtype=x.dtype) 
        for k, grad_k in enumerate(x_grad):
            tmp_grad = gradient(grad_k) 
            for l, grad_kl in enumerate(tmp_grad):
                hessian[k, l, :, :] = grad_kl
        return hessian
        
    def Gradient(self,x):
        if grad!=None:
            return grad
        else:
            return gradient()
                        
    
class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        