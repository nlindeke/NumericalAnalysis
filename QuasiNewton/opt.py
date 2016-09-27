from numpy import *
from scipy import *
from itertools import *

def f(x):
    return (2*x[0]**3-10*x[1]**2)/(5-x[2]**2)
def f2(x):
    return 3*x[0]**4+2*x[1]**5
def f3(x):
    return 5*x[0]**3-10*x[1]**2
    
def Rosenbrock(x):
    return 100*(x[1]-x[0]**2)**2+(1-x[0])**2

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
        #error handling, maybe do this check when we have actual values to check :))
        try:
            a=numpy.linalg.cholesky(matrice)
        except LinAlgError as e:
            print("not positive-definite: ",e)
        
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
      
    #Line search for getting alfa_k as in the lecture slides with a nifty function I found in scipy.optimize
    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html#scipy.optimize.minimize_scalar
    #check the example at the bottom, seems to look ok, haven't actually tested it yet :)))
    def LineSearch(self,x,s):
        alfa_k=f(x+alfa*s)
        return minimize_scalar(alfa_k).x
        
    def f_der(self,x):
        h=10**-8
        return (f(x+h)-f(x))/h
        
    def InexactLineSearch(self,x,s,rho=0.1,sigma=0.7,tau=0.1,X=9):
        alfa_L=0 #define starting interval a_0 ∈ [a_L,a_U]
        alfa_U=10**99
        alfa_0=1
        def f_a(x,s,alfa):
            return f(x+alfa*s)
            
        def extrapolate(alfa_0,_alfa_L):
            return stuff
            
        def interpolate(alfa_0,_alfa_U):
            return stuff

        LC = f_a(alfa_0)>=f_(alfa_L)+(1-rho)*(alfa_0-alfa_L)*f_der(alfa_L)       
        RC = f_a(alfa_0)<=f_(alfa_L)+rho*(alfa_0-alfa_L)*f_der(alfa_L)
        
        while not (LC and RC):
            if (not LC):
                d_alfa_0=extrapolate(alfa_0,alfa_L)
                d_alfa_0=numpy.max([d_alfa_0,tau*(alfa_0-alfa_L)])
                d_alfa_0=numpy.min([d_alfa_0,X*(alfa_0-alfa_L)])
                alfa_L=alfa_0
                alfa_0=alfa_0+d_alfa_0
            else:
                alfa_U=numpy.min(alfa_0,alfa_U)
                alfa_hat=interpolate(alfa_0,alfa_U)
                alfa_hat=numpy.max([alfa_hat,alfa_L+tau*(alfa_U-alfa_L)])
                alfa_hat=numpy.min([alfa_hat,alfa_U-tau*(alfa_U-alfa_L)])
                alfa_0=alfa_hat
            #calculate new f_a(alfa_L),f_a(alfa_0)
            LC=f_a(alfa_0)>=f_(alfa_L)+(1-rho)*(alfa_0-alfa_L)*f_der(alfa_L)
            RC=f_a(alfa_0)<=f_(alfa_L)+rho*(alfa_0-alfa_L)*f_der(alfa_L)
        return alfa_0,f(alfa_0)
    
class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False
        