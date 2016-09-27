from numpy import *
from scipy import *
from itertools import *

def f(x):
    return (2*x[0]**3-10*x[1]**2)/(5-x[2]**2)
def f2(x):
    return 3*x[0]**4+2*x[1]**5
def f3(x):
    return 5*x[0]**3-10*x[1]**2

def grad(f,x):
    h=10**(-8)
    dim=len(x)
    e=identity(dim)
    arr=zeros((1,dim))
    for i in range(dim):
        arr[0][i]=(f(x+h*e[:][i])-f(x))/h
    return arr
def besthessian(f,x):
    h=10**(-8)
    dim=len(x)
    e=identity(dim)
    arr=empty((dim,dim))
    for i in range(dim):
        arr[i][:]=array(((grad(f,x+h*e[:][i])-grad(f,x))/h))
    return arr
    
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
    def computefuncneu(self,dim,nbvalues=1000,step=1):
        #We decide the dimension to be 2 for the time being
        f=self.obj_func
        matricevaleurs=zeros((nbvalues,nbvalues))
        for i in itertools.product(range(nbvalues),dim):
                matricevaleurs[i][j]=f(i*step,j*step)
        return matricevaleurs
    
    def gradientmaison(self,dim,point,nbvalues):
        matricefinale=zeros((nbvalues,nbvalues))
        matricevaleurs=computefunc(self.obj_func,10)
        for i in range(nbvalues):
            for j in range(nbvalues):
                matricefinale[i][j]=None
        None
      
    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html#scipy.optimize.minimize_scalar
    #check the example at the bottom, seems to look ok, haven't actually tested it yet :)))
    def LinearSearch(self,x,s):
        alfa_k=f(x+alfa*s)
        return minimize_scalar(alfa_k).x
    
class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        