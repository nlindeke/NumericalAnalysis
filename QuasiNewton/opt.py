from numpy import *
from scipy import *

def f(x,y):
    return 2*x**2+3*y**2
def dimgrid(dim,nbvalues=1000):
    A=zeros((nbvalues,dim))
    for i in range(dim):
        for j in range (nbvalues):
            A[j][i]=j
    return A
def computefunc(f,nbvalues=1000):
    matricevaleurs=zeros((nbvalues,nbvalues))
    for j in range(nbvalues):
        for i in range(nbvalues):
            matricevaleurs[j][i]=f(j,i)
    return matricevaleurs
def gradientmaison(f,dim,point):
    return f()
    
    
def grad():
    h = 0.001
    space = 10
    grad = empty(space)
    for x in range(0,space):
        grad[x] = (f(x+h)-f(x-h))/2*h
    return grad

def dfdx():
    grad = gradient(f(2))
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
        termination_criterion=False
        while termination_criterion!=True:
            x=x-self.NewtonDirection(x)
            if x<=0.0001 and x>=-0.0001:
                termination_criterion=True
        return x
    def NewtonDirection(self,x):
        return self.InvHessian(x)*self.Gradient(x)
        
    def InvHessian(self,x):
        return linalg.inv(hessian())
        
    def hessian(self,x):
        x = obj_func
        x_grad = gradient(x) 
        hessian = empty((x.ndim, x.ndim) + x.shape, dtype=x.dtype) 
        for k, grad_k in enumerate(x_grad):
            tmp_grad = gradient(grad_k)
            for l, grad_kl in enumerate(tmp_grad):
                hessian[k, l, :, :] = grad_kl
        return hessian
    def betterhessian(self,grad):
        dim=shape(grad)[0]
        matrice=zeros(dim,dim)
        for i in range(dim):
            for j in range(dim):
                matrice[i][j]=None
        
    def Gradient(self,x):
        if self.grad!=None:
            return self.grad
        else:
            return gradient(x)
                        
    
class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        