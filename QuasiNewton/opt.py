from numpy import *
from scipy import *

def f(x,y,z):
    return (2*x**3-10*y**2)/(5-z**2)
    
def grad():
    h = 0.001
    space = 10
    grad = empty(space) #what are we living for
    for x in range(0,space):
        grad[x] = (f(x+h)-f(x-h))/2*h
    return grad

def multigrad(f):
    h=0.0001
    space = 10
    grad = zeros((3,space))

    for x in range(0,space):
        grad[0][x] = (f(x+h,1,1)-f(x-h,1,1))/2*h
        grad[1][x] = (f(1,x+h,1)-f(1,x-h,1))/2*h
        grad[2][x] = (f(1,1,x+h)-f(1,1,x-h))/2*h        

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
            
    def dimgrid(self,dim,nbvalues=1000,step=1):
        A=zeros((nbvalues,dim))
        for i in range(dim):
            for j in range (nbvalues):
                A[j][i]=j*step
        return A
    def computefunc(self,nbvalues=1000,step=1):
        #We decide the dimension to be 2 for the time being
        f=self.obj_func
        matricevaleurs=zeros((nbvalues,nbvalues))
        for i in range(nbvalues):
            for j in range(nbvalues):
                matricevaleurs[i][j]=f(i*step,j*step)
        return matricevaleurs
    
    def gradientmaison(self,dim,point,nbvalues):
        matricefinale=zeros((nbvalues,nbvalues))
        matricevaleurs=computefunc(self.obj_func,10)
        for i in range(nbvalues):
            for j in range(nbvalues):
                matricefinale[i][j]=None
        None
    
class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        