from numpy import *
from scipy import *
from itertools import *

def f(x):
    return (2*x[0]**3-10*x[1]**2)/(5-x[2]**2)
def f2(x):
    return 3*x[0][0]**4+2*x[0][1]**5
def f3(x):
    return (5*(x[0][0])**3)-(10*(x[0][1])**2)

    
class OPC:
    """
    Some stuff
    """
    def __init__(self, obj_func, gradis=None):
        self.obj_func = obj_func
        self.gradis = gradis
        
    def base_newton(self,xzero):
        x=self.listtoarray(xzero)
        termination_criterion=False
        k=0
        #try:
        while termination_criterion!=True:
            k+=1
            x[0]=x[0]-self.NewtonDirection(x)
            if sum(x)<=0.0001 and sum(x)>=-0.0001:
                termination_criterion=True
        #except linalg.linalg.LinAlgError:
        #    return None
        return k
    
    def NewtonDirection(self,x):
        return array(transpose(matrix(self.InvHessian(x))*matrix(transpose(self.Gradient(x)))))
    def NewtonDirection2(self,x):
        return array(transpose(-1*matrix(self.besthessian(x))*matrix(transpose(self.Gradient(x)))))

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
        h=10**(-3)
        dim=len(x[0])
        e=identity(dim)
        arr=zeros((1,dim))
        for i in range(dim):
            arr[0][i]=(f(x+h*e[:][i])-f(x-h*e[:][i]))/(2*h)
        return arr

    def besthessian(self,x):
        f=self.obj_func
        h=10**(-3)
        dim=len(x[0])
        e=identity(dim)
        arr=empty((dim,dim))
        for i in range(dim):
            # print(array(((self.grad(x+h*e[:][i])-self.grad(x-h*e[:][i]))/(2*h))))
        
            print(array(((self.grad(x+h*e[:][i])-self.grad(x-h*e[:][i]))/(2*h))))
            arr[i][:]=array(((self.grad(x+h*e[:][i])-self.grad(x-h*e[:][i]))/(2*h)))
                #error handling
        """try:
            linalg.cholesky(arr)
        except linalg.linalg.LinAlgError as e:
            print("not positive-definite: ",e)"""
        return arr

    def listtoarray(self,x):
        dim=len(x)
        matrice=zeros((1,dim))
        for i in range(dim):
            matrice[0][i]=x[i]
        return matrice
        
    def LineSearch(self,x,s):
        alfa_k=f(x+alfa*s)
        return minimize_scalar(alfa_k).x
        
        
    def InexactLineSearch(self,x,s,rho=0.1,sigma=0.7,tau=0.1,X=9):
        alfa_L=0 #define starting interval a_0 ∈ [a_L,a_U]
        alfa_U=10**99
        alfa_0=1
        def f_a(x,s,alfa):
            return f(x+alfa*s)
            
        def extrapolate(alfa_0,_alfa_L):
            return (alfa_0-alfa_L)*(f_der(alfa_0)/(f_der(alfa_L)-f_der(alfa_0)))
            
        def interpolate(alfa_0,_alfa_U):
            return ((alfa_0-alfa_L)**2)*f_der(alfa_L)/(2*(f_a(alfa_L)-f_a(alfa_0)*f_der(alfa_L)))
           
        def f_der(self,x):
            h=10**(-8)
            return (f_a(x+h)-f_a(x))/h

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
        return alfa_0,f_a(alfa_0)

class QN(OPC):
    def __call__(self):
        return False

class E(OPC):
    def __call__(self):
        return False
    
class IE(OPC):
    def __call(self):
        return False

class BadBroyden(OPC):
    def __init__(self):
        super(BadBroyden,self).__init__()
        
class GoodBroyden(OPC):
    def __init__(self):
        super(GoodBroyden,self).__init__()
        
class DFP(OPC):
    None
class BFGS(OPC):
    None