from numpy import *
from scipy import *
from itertools import *

def f(x):
    return (2*x[0]**3-10*x[1]**2)/(5-x[2]**2)
def f2(x):
    return 3*x[0]**4+2*x[1]**5
def f3(x):
    return 5*x[0]**3-10*x[1]**2

    
class OPC:
    """
    Some stuff
    """
    def __init__(self, obj_func, gradis=None):
        self.obj_func = obj_func
        self.gradis = gradis
        
    def base_newton(self,xzero):
        x=xzero
        termination_criterion=False
        while termination_criterion!=True:
            x=x-self.NewtonDirection(x)
            if x.any()<=0.0001 and x.any()>=-0.0001:
                termination_criterion=True
        return x
    
    def NewtonDirection(self,x):
        return transpose(matrix(self.InvHessian(x))*matrix(transpose(self.Gradient(x))))
        
    def InvHessian(self,x):
        return linalg.inv(self.besthessian(x))
       
    def Gradient(self,x):
        if self.gradis!=None:
            return self.gradis
        else:
            return self.grad(x)
            
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
    
    def grad(self,x):
        f=self.obj_func
        h=10**(-8)
        dim=len(x)
        e=identity(dim)
        arr=zeros((1,dim))
        for i in range(dim):
            arr[0][i]=(f(x+h*e[:][i])-f(x))/h
        return arr
    def besthessian(self,x):
        f=self.obj_func
        h=10**(-8)
        dim=len(x)
        e=identity(dim)
        arr=empty((dim,dim))
        for i in range(dim):
            arr[i][:]=array(((self.grad(x+h*e[:][i])-self.grad(x))/h))
        return arr

class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        