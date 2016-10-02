from numpy import *
from scipy import *
import scipy.linalg as lin
from scipy.optimize import minimize, rosen, rosen_der
#Projet of Niklas Lindeke, Laroy Sjödahl, Charles Rohart and Ingrid Odlen

#List of functions to test the code
def f1(x):
    return (2*x[0]**3-10*x[1]**2)/(5-x[2]**2)
def f2(x):
    return 3*x[0][0]**4+2*x[0][1]**5
def f3(x):
    return (2*(x[0][0])**3)-(10*(x[0][1])**2)
def f4(x): #Rosenbrock function
    return (100*(x[0][1]-x[0][0]**2)**2)+((1-x[0][0])**2)


x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
res = minimize(rosen, x0, method='BFGS', tol=1e-6)
    
class OPC:
    """
    The general class containing implementation of:
        - Gradient
        - Hessian
        - Direction Based on the Newton Method
        - Exact and Inexact Line Search
    Input of class is one of the four pre-defined function f1-f4
    """
    def __init__(self, obj_func, gradis=None):
        self.obj_func = obj_func
        self.gradis = gradis
        self.h_glob = 10**(-4)
        
    def base_newton(self,xzero):
        """
        Implementation of the Base Method in the Newton Iteration
        """
    
        x=self.listtoarray(xzero)
        termination_criterion=False
        k=0
        try:
            while termination_criterion!=True:
                k+=1
                x[0]=x[0]-self.NewtonDirection(x)
                if sum(x)<=0.0001 and sum(x)>=-0.0001:
                    termination_criterion=True
        except linalg.linalg.LinAlgError:
            return None
        return k
    
    def NewtonDirection(self,x):
        return array(transpose(matrix(self.InvHessian(x))*matrix(transpose(self.Gradient(x)))))
        
    def NewtonDirection2(self,x): #useless, besthessian should also be inverse, don't use
        return array(transpose(-1*matrix(self.besthessian(x))*matrix(transpose(self.Gradient(x)))))
        
    def InvHessian(self,x):
        """
        Evaluate the inverse of the Hessian
        """
        return linalg.inv(self.besthessian(x))
        
    def Gradient(self,x):
        """
        Function to recieve possible pre-defined Gradient vector
        rarely used as we saw that our grad-function using 
        the centered finite difference formula has good accuracy
        """
        if self.gradis!=None:
            return self.gradis
        else:
            return self.grad(x) 
    """
    dimgrid and computefunc are legacy functions that were used to create values
    to compute onto
    """
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
        """
        Function evaluating the n-dimensional Gradient vector by using the
        centered finite difference formula
        """
        f=self.obj_func
        h=self.h_glob
        dim=len(x[0])
        e=identity(dim)
        arr=zeros((1,dim))
        for i in range(dim):
            arr[0][i]=(f(x+h*e[:][i])-f(x-h*e[:][i]))/(2*h)
        return arr

    def besthessian(self,x):
        """
        Function evaluating the Hessian of an n-dimensional
        objective function taking the Jacobian of the Gradient vector
        """
        f=self.obj_func
        h=self.h_glob
        dim=len(x[0])
        e=identity(dim)
        arr=empty((dim,dim))
        for i in range(dim):
            arr[i][:]=array(((self.grad(x+h*e[:][i])-self.grad(x-h*e[:][i]))/(2*h)))
        return arr

    def listtoarray(self,x):
        """
        Function which transforms the input values in x into
        a matrix that is more easy to work with
        """
        dim=len(x)
        matrice=zeros((1,dim))
        for i in range(dim):
            matrice[0][i]=x[i]
        return matrice
        
    def ExactLineSearch(self,x,s):
        """
        Implementation of the Exact Line Search Method
        """
        alfa = 0
        alfa_k=f3(x+alfa*s)
        return minimize_scalar(alfa_k).alfa

    def InexactLineSearch(self,x,s,rho=0.1,sigma=0.7,tau=0.1,X=9):
        """
        Implementation of the Inexact Line Search Method
        """        
        #x = self.listtoarray(xx)
        #s = -self.NewtonDirection(x)
        alfa_L=0 #define starting interval a_0 ∈ [a_L,a_U]
        alfa_U=10**9
        alfa_0=1
        d_alfa_0=0
        alfa_hat=0
        def f_a(x_in,s_in,alfa):
            return f3(x_in+alfa*s_in)
            
        def extrapolate(x_in,s_in,a_0,_a_L):
            temp =(f_der(x_in,s_in,_a_L)-f_der(x_in,s_in,a_0))
            if temp == 0:
                temp=0.000001
            return (a_0-_a_L)*(f_der(x_in,s_in,a_0)/temp)
            
        def interpolate(x_in,s_in,a_0,a_L):
            return ((a_0-a_L)**2)*f_der(x_in,s_in,a_L)/(2*(f_a(x_in,s_in,a_L)-f_a(x_in,s_in,a_0)*f_der(x_in,s_in,a_L)))
           
        def f_der(x_in,s_in,a_0):
            h=10**(-3)
            return (f_a(x_in+h,s_in,a_0)-f_a(x_in,s_in,a_0))/h

        LC = f_a(x,s,alfa_0)>=f_a(x,s,alfa_L)+(1-rho)*(alfa_0-alfa_L)*f_der(x,s,alfa_L)       
        RC = f_a(x,s,alfa_0)<=f_a(x,s,alfa_L)+rho*(alfa_0-alfa_L)*f_der(x,s,alfa_L)
        count=1
        alfa_old=0
        while not (LC and RC):
            if (not LC):
                #print("LC is false")
                d_alfa_0=extrapolate(x,s,alfa_0,alfa_L)
                d_alfa_0=max([d_alfa_0,tau*(alfa_0-alfa_L)])
                d_alfa_0=min([d_alfa_0,X*(alfa_0-alfa_L)])
                alfa_L=alfa_0
                alfa_0=alfa_0+d_alfa_0
                if abs(alfa_0-alfa_old)<0.0000001: #the change is fucking small, it drives me crazy, i don't know what's going on
                    break
                alfa_old=alfa_0
            else:
                #print("LC is true")
                alfa_U=min([alfa_0,alfa_U])
                alfa_hat=interpolate(x,s,alfa_0,alfa_L)
                alfa_hat=max([alfa_hat,alfa_L+tau*(alfa_U-alfa_L)])
                alfa_hat=min([alfa_hat,alfa_U-tau*(alfa_U-alfa_L)])
                alfa_0=alfa_hat
            LC=f_a(x,s,alfa_0)>=f_a(x,s,alfa_L)+(1-rho)*(alfa_0-alfa_L)*f_der(x,s,alfa_L)
            RC=f_a(x,s,alfa_0)<=f_a(x,s,alfa_L)+rho*(alfa_0-alfa_L)*f_der(x,s,alfa_L)
        return alfa_0,f_a(x,s,alfa_0)

class QN(OPC):
    """
    Quasi-Newton Optimization Class which implements the 
    actual Quasi-Newton process based on the information 
    gathered from the OPC class
    
    Input one of pre-defined functions f1-f4 and utilize
    iteration function which takes an initial array 
    guess of x_i values
    
    """
    def Iterate(self,guess,lineSearchVariant=None,UpdateVariant=None,NumOfIterations=None):
        if NumOfIterations==None:
            NumOfIterations=100
            
        def ChosenLineSearch(x,s):
            """
            Depending on input "lineSearchVariant" in the parent funcion
            ChosenLineSeach will return either the Exact Linesearch Method
            or the Inexact Linesearch Method
            """
            if lineSearchVariant=="exact":
                return self.ExactLineSearch(x,s)
            elif lineSearchVariant=="inexact":
                return self.InexactLineSearch(x,s)[0]
    
        def ChosenUpdate(iH,g,d):
            """
            Receives some string to chose between four different update methods
            """
            if UpdateVariant=="good":
                return GoodBroyden.Update(iH,g,d)
            elif UpdateVariant=="bad":
                return BadBroyden.Update(iH,g,d)
            elif UpdateVariant=="dfp":
                return DFP.Update(iH,g,d)
            elif UpdateVariant=="bfgs":
                return BFGS.Update(iH,g,d)
            else:
                print("Err")
        x=self.listtoarray(guess)
        invH=self.InvHessian(x)
        counter=1
        for i in range(NumOfIterations):
            grad=self.Gradient(x).T
            s=-self.InvHessian(x)*grad #step 1
            alfa=ChosenLineSearch(x,s) #step 2
            next_x= x + (alfa*s) #step 3
            delta=next_x-x
            next_grad=self.Gradient(next_x)
            gamma=next_grad-grad
            x=next_x #prepare for next iteration
            if(lin.norm(grad)<0.01):
                return x
            invH=ChosenUpdate(invH,gamma,delta)# step 4: update the hessian
            counter=counter+1
        return x

class GoodBroyden(QN):
    """
    Class implementing the Good Broyden method depending on the QN parent class
    """    
    #i think this works
    def Update(invH,gamma,delta):
        u=delta-dot(invH,gamma)
        u_T=u.T
        a=1/dot(u_T,gamma)
        H_k=invH+a*dot(u,u_T)
        return H_k

class BadBroyden(QN):
    """
    Class implementing the Bad Broyden method depending on the QN parent class
    """
    def Update(invH,gamma,delta):
        #slide 54? straight codified version, anyway, does not work
        return invH+divide((gamma-invH*delta),(transpose(delta)*delta))*transpose(delta)
        
class BFGS(QN):
    """
    Class implementing the BFGGS method depending on the QN parent class
    """    
    def Update(invH,gamma,delta):
        return invH+(1+(transpose(gamma)*invH*gamma)/(transpose(delta)*gamma))*((delta*transpose(delta))/(transpose(delta)*gamma))\
        -(delta*transpose(delta)*invH+invH*gamma*transpose(delta))/(transpose(delta)*gamma)

class DFP(QN):
    """
    Class implementing the DFP method depending on the QN parent class
    """    
    def Update(invH,gamma,delta):
        return invH+((delta*transpose(delta))/(transpose(delta)*gamma))-((invH*gamma*transpose(gamma)*invH)/(transpose(gamma)*invH*gamma))